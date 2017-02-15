function success(data) {
  $("#id_username").val(data['uname']);
  $("#id_firstname").val(data['firstname']);
  $("#id_lastname").val(data['lastname']);
  $("#id_email").val(data['email']);
  $("#id_address").val(data['address']);
  $("#id_city").val(data['city']);
  $("#id_country").val(data['country']);
  $("#id_pincode").val(data['pincode']);
  $("#id_aboutme").val(data['aboutme']);
}

$(document).ready(function () {
  $.getJSON("/getprofiledata/", "", success);

});
