
$(document).ready(function(){
    $("#submit").click(function(){
      var lblmsg=document.getElementById("error-message");
        if($("#activityname").val()=='')
        {
          lblmsg.innerHTML="Activity Name Required";
          return false;
        }
        if($("#activitytype").val()=='')
        {
          lblmsg.innerHTML="Activity Type Required";
          return false;
        }

        if($("#duration").val()=='')
        {
          lblmsg.innerHTML="Duration Required";
          return false;
        }
        if($.isNumeric($('#duration').val()) == false)
        {
          lblmsg.innerHTML="Invalid Duration ";
          return false;
        }
        if($("#repeats").val()=='')
        {
          lblmsg.innerHTML="Repeats Required";
          return false;
        }
        jQuery.ajax({
          url: "../task/create",
          type: "post",
          dataType: 'json',
          cache : false,
          contentType: "application/json; charset=utf-8",
          data: JSON.stringify( {"data": {"activityname" : $('#activityname').val(), "taskid":$('#taskid').val()}} ),
          success: function(msg) {
              window.location = msg   
          }
        });
    });  
      
});