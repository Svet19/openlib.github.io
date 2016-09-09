$.urlParam = function(name) {
  var results = new RegExp('[\?&]' + modelID + '=([^&#]*)').exec(window.location.href);
  if (results==null) {
    return null;
  }
  else{
    return results[1] || 0;
  }
}

$(document).ready( function() {
  if ($.urlParam('modelID') != '') {
    $.get( "http://174.27.114.24/gmlc-demo/getModelInfo.cgi?" + $.urlParam('modelID'), function( data ) {
      $(#modelName).html(data.modelName);  
    });        
  }
};
