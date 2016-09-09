#!/usr/bin/perl -wT 

use CGI;
use CGI::Carp qw(fatalsToBrowser);
my $CGI = CGI->new;
use JSON;
use Data::Dumper;

my $params = $CGI->Vars;

print "Content-Type: application/json\n\n";

use DBI;
use DBD::mysql;
#require './lib/mysqlCredentials.pl';
#my ($username, $password) = mysqlCredentials();

if (exists $params->{modelID} and $params->{modelID} ne '') {
	my $db = DBI->connect("dbi:mysql:gmlc-modelinfo:localhost:3306", 'mysqluser', '') || die "cannot connect";
	my $query = $db->prepare("select * from `ModelInfo` where `modelID` = ?");
	$query->execute($params->{modelID});
	$result = $query->fetchrow_hashref();
	$db->disconnect();
	if (!$result) {
		$result = {"modelID" => "...NOT FOUND...", "modelName" => "", "authorName"=>"", "authorOrg"=>""};
	}
}
else {
	$result = {"modelID" => "", "modelName" => "", "authorName"=>"", "authorOrg"=>""};
}

my $json = JSON->new;
print $json->encode($result);
