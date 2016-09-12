$.urlParam = function(name) {
  var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
  if (results==null) {
    return null;
  }
  else{
    return results[1] || 0;
  }
}

$(document).ready( function() {
  if ($.urlParam('modelID') != null) {
    $.getJSON( "./getModelInfo.cgi?modelID=" + $.urlParam('modelID'), function(data, status) {
      $("#modelName").html(data.modelName);  
      $("#author").html(data.authorName + " / " + data.authorOrg);  
      $("#date").html(data.date);  
      $("#version").html(data.version);  
      $("#accessibility").html(data.accessibility);  
      $("#proprietary").html(data.proprietary);  
      $("#symbol").html(data.symbol);  
      $("#accreditation").html(data.accreditation);  
      $("#type").html(data.type);  
      $("#background").html(data.background);  
      $("#specifications").html(data.specifications);  
      $("#dependencies").html(data.dependencies);  
      $("#interfacing").html(data.interfacing);  
      $("#diagram").html(data.diagram);  
      $("#hil").html(data.hilCapabilities + data.hilDiagram);  
    });        
  }
});
