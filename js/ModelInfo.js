ModelInfo = 
[{"Org":"INL","Name":"IEEE 13 node distribution test feeder [ieee13node]","Platform":"RSCAD","Category":"Distribution Grid","Type":"Model","ID":"10000001"},
 {"Org":"INL","Name":"Test Model - Rahul and Sveto","Platform":"Python","Category":"HVAC","Type":"Model","ID":"10000099"},
 {"Type":"Model","ID":"10000002","Org":"ORNL","Name":"Hospital HVAC model","Category":"HVAC","Platform":"Labview"},
 {"Category":"Residential Appliances","Platform":"Python","Name":"Residential home probabilistic load model","Org":"NREL","ID":"10000003","Type":"Model"},
 {"Category":"Commercial Non-HVAC","Platform":"Python","Name":"Large machine shop model","Org":"LBNL","ID":"10000004","Type":"Model"},
 {"Type":"Model","ID":"10000005","Org":"NREL","Name":"Parking structure PV panel model","Category":"PV Panel","Platform":"Matlab"},
 {"Platform":"Labview","Category":"Inverter","Name":"Inverter model with transient load capability","Org":"NREL","ID":"10000006","Type":"Model"},
 {"Type":"Model","ID":"10000007","Category":"Battery","Platform":"Labview","Org":"SNL","Name":"Lead acid battery storage system"},
 {"Type":"Model","ID":"10000008","Org":"SNL","Name":"Battery powered load leveling inverter","Category":"Inverter","Platform":"Matlab"},
 {"Type":"Model","ID":"10000009","Org":"ANL","Name":"Electric vehicle charging depot model","Platform":"Matlab","Category":"Electric Vehicle"},
 {"Org":"INL","Name":"Supercapacitor regenertive braking model","Category":"Supercapacitor","Platform":"Labview","Type":"Model","ID":"10000010"},
 {"ID":"10000011","Type":"Model","Name":"Large underground flywheel storage model","Org":"INL","Category":"Flywheel","Platform":"Matlab"},
 {"Category":"Fuel Cell","Platform":"Python","Name":"Photoelectrochemical fuel cell model","Org":"INL","ID":"10000012","Type":"Model"},
 {"Platform":"Python","Category":"Electrolyzer","Org":"INL","Name":"Large scale PEM Electrolyzer model","Type":"Model","ID":"10000013"},
 {"Name":"Bedrock heat exchanger model","Org":"PNNL","Category":"Thermal Storage","Platform":"Matlab","ID":"10000014","Type":"Model"},
 {"Org":"PNNL","Name":"400kV Transmission grid with disturbance analysis","Platform":"Matlab","Category":"Transmission Grid","Type":"Model","ID":"10000015"}
];

$(document).ready( function() {
	$(".filter-selectors").change( function() {
		filltable();
	}); 
});
 
function filltable() {
	myhtm = "<table><tbody><tr><th width=\"80px\">ID</th><th width=\"40px\">Org</th><th width=\"60px\">Type</th><th width=\"200px\">Category</th><th width=\"100px\">Platform</th><th width=\"500px\">Name</th><th width=\"100px\">Summary</th><th width=\"100px\">Link</th></tr>";
	numberin = 0;
	ModelInfo.forEach( function(element) {
		itsin = 1;
		if ( ! $("#selector1").val() ) {
			itsin1 = 1;
		}
		else {
			itsin1 = 0;
			$("#selector1").val().forEach( function(value) {
				if (element.Org === value) {
					itsin1 = 1;
				}
			});
		}
		itsin *= itsin1;
		if ( ! $("#selector2").val() ) {
			itsin2 = 1;
		}
		else {
			itsin2 = 0;
			$("#selector2").val().forEach( function(value) {
				if (element.Type === value) {
					itsin2 = 1;
				}
			});
		}
		itsin *= itsin2;
		
		if ( ! $("#selector3").val() ) {
			itsin3 = 1;
		}
		else {
			itsin3 = 0;
			$("#selector3").val().forEach( function(value) {
				if (element.Category === value) {
					itsin3 = 1;
				}
			});
		}
		itsin *= itsin3;
		
		if ( ! $("#selector4").val() ) {
			itsin4 = 1;
		}
		else {
			itsin4 = 0;
			$("#selector4").val().forEach( function(value) {
				if (element.Platform === value) {
					itsin4 = 1;
				}
			});
		}
		itsin *= itsin4;

		if (itsin) {
			numberin += 1;
			myhtm += "<tr><td>" + element.ID + "</td><td>" + element.Org + "</td><td>" + element.Type + "</td><td>" + element.Category + "</td><td>" + element.Platform + "</td><td>" + element.Name + "</td><td><a target=\"_blank\" href=\"testTemplate.html\">Summary</a></td><td><a target=\"_blank\" href=\"ModelInfoTemplate.html?modelID=10000001\">Download</a></td></tr>";
		}	
	});
	myhtm += "</tbody></table>";
	$("#num-found").html(numberin);
	$("#selector-results").html(myhtm);
}
