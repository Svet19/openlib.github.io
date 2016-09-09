gmlc-database;
require Exporter;
@ISA = ("Exporter");
#@EXPORT = qw//;
@EXPORT = qw/new Result OpenDB QueryDB CloseDB/;

use v5.14.2;
use strict;
use URI::Escape;
use constant _REV => "gmlc-database v1.0";

sub new {
	#Instantiates a new DscCommonForm object
	my ($class, $self) = @_;
	bless($self, $class);
	$self->{'DBisOpen'} = 0;
	return $self;
}

sub Result {
	#Return response to client
	use JSON;
	my $self = shift;
	my $json = JSON->new;
	print "Content-Type: application/json\n\n";
	my $time;
	if ($self->{'Success'}) {
		$time = $self->{PassTimer};
	}
	else {
		$self->CloseDB;
		$time = $self->{FailTimer};
	}
	my $result = 	{	
				Success => $self->{Success},
				Time => $time,
				URL => $self->{URL},
				Message => $self->{'Message'},
			};
	$result->{ErrMsg} = join('<br/>',@{$self->{errmsg}}) if scalar @{$self->{errmsg}};
	print $json->encode($result);
	return 1;
}

sub OpenDB {
	#Connect to database
	my $self = shift;
	my $database = shift || "gmlc-modelinfo";
	unless ($self->{DBisOpen}) {
		use DBI;
		use DBD::mysql;
		require 'mysqlCredentials.pl';
		my ($username, $password) = mysqlCredentials();
		my $db = "dbi:mysql:$database:localhost:3306";
		$self->{DB} = DBI->connect($db, $username, $password)
			|| do { push(@{$self->{errmsg}}, "Cannot connect to database."); return 0;};
		if ($self->{DB}->err()) {
			push(@{$self->{errmsg}}, "Cannot connect to database.");
			$self->{DB}->disconnect();
			$self->{DB} = undef; 
			$self->{DBisOpen} = 0;
			return 0;
		}
	}
	$self->{DBisOpen} = 1;
	return 1;
}

sub CloseDB {
	my $self = shift;
	if ($self->{DBisOpen}) {
			$self->{DB}->disconnect();
			$self->{DB} = undef; 
			$self->{DBisOpen} = 0;
			return 1;
	}
	return 0;
}

sub QueryDB {
	my $self = shift;
	my $querystring = shift;
	my $arguments = shift || [];
	$self->OpenDB || return 0;
	my $query = $self->{DB}->prepare($querystring);
	$query->execute(@{$arguments});
	if ($self->{DB}->err()) {
		return 0;
	}
	return $query;
}

1;
