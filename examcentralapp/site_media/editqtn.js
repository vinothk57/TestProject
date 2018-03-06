function showqtnedit(result) {
    console.log(JSON.stringify(result));
    $('#id_examid').val(result['examid']);
    $('#id_qno').val(result['qno']);
    $('#id_qno').attr("readonly", true);
    $('#id_question').val(result['question']);
    $('#id_qtype').val(result['qtype']);
    $('#id_qcategory').val(result['qcategory'].toString());
    $('#id_optionA').val(result['optionA']);
    $('#id_optionB').val(result['optionB']);
    $('#id_optionC').val(result['optionC']);
    $('#id_optionD').val(result['optionD']);
    $('#id_optionE').val(result['optionE']);
    $('#id_isOptionA').prop("checked", result['isOptionA']);
    $('#id_isOptionB').prop("checked", result['isOptionB']);
    $('#id_isOptionC').prop("checked", result['isOptionC']);
    $('#id_isOptionD').prop("checked", result['isOptionD']);
    $('#id_isOptionE').prop("checked", result['isOptionE']);
    $('#id_haspic').prop("checked", result['haspic']);
    $('#hasdirection').prop("checked", result['hasdirection']);
    $('#id_answer').val(result['answer']);
    if (result['hasdirection']) {
        tinymce.get("id_direction").execCommand('mceSetContent', false, result['direction']);
    } else {
        tinymce.get("id_direction").execCommand('mceSetContent', false, '');
    }
}

function showqtnpreview(result) {
    console.log(JSON.stringify(result));
    if(result['hasdirection']) {
        console.log(result['direction']);
        $('#direction_qview').html(result['direction']);
    } else {
        $('#direction_qview').text('');
    }
    if(result['haspic']) {
        $('#img_qview').attr("src",result['picpath']);
    } else {
        $('#img_qview').attr("src", "");
    }
    var qstring = "<h6>" + result['qno'] + ". " + result['question'] + "</h6>";

    var options = "";
    if(result['qtype'] == "1") {
        if(result['optionA'] != "") {
          options = options + "<div class=\"form-group radio-pink-gap\">";
          options = options + "<input type=\"radio\" name=\"option\" class=\"with-gap\" style=\"vertical-align:top\"";
        if(result['isOptionA']) {
          options = options + "checked = \"checked\" ";
        }
        options = options + "><label style=\"padding-left:5px; width:90%; font-weight:normal;\">" + result['optionA'] + "</label></div>";
        }

        if(result['optionB'] != "") {
          options = options + "<div class=\"form-group radio-pink-gap\">";
          options = options + "<input type=\"radio\" name=\"option\" class=\"with-gap\" style=\"vertical-align:top\"";
        if(result['isOptionB']) {
          options = options + "checked = \"checked\" ";
        }
        options = options + "><label style=\"padding-left:5px; width:90%; font-weight:normal;\">" + result['optionB'] + "</label></div>";
        }

        if(result['optionC'] != "") {
          options = options + "<div class=\"form-group radio-pink-gap\">";
          options = options + "<input type=\"radio\" name=\"option\" class=\"with-gap\" style=\"vertical-align:top\"";
        if(result['isOptionC']) {
          options = options + "checked = \"checked\" ";
        }
        options = options + "><label style=\"padding-left:5px; width:90%; font-weight:normal;\">" + result['optionC'] + "</label></div>";
        }

        if(result['optionD'] != "") {
          options = options + "<div class=\"form-group radio-pink-gap\">";
          options = options + "<input type=\"radio\" name=\"option\" class=\"with-gap\" style=\"vertical-align:top\"";
        if(result['isOptionD']) {
          options = options + "checked = \"checked\" ";
        }
        options = options + "><label style=\"padding-left:5px; width:90%; font-weight:normal;\">" + result['optionD'] + "</label></div>";
        }

        if(result['optionE'] != "") {
          options = options + "<div class=\"form-group radio-pink-gap\">";
          options = options + "<input type=\"radio\" name=\"option\" class=\"with-gap\" style=\"vertical-align:top\"";
        if(result['isOptionE']) {
          options = options + "checked = \"checked\" ";
        }
        options = options + "><label style=\"padding-left:5px; width:90%; font-weight:normal;\">" + result['optionE'] + "</label></div>";
        }
    } else if (result['qtype'] == "3") {
        if(result['optionA'] != "") {
          options = options + "<div class=\"form-group radio-pink-gap\">";
          options = options + "<input type=\"checkbox\" name=\"option\" class=\"with-gap\" style=\"vertical-align:top\"";
        if(result['isOptionA']) {
          options = options + "checked = \"checked\" ";
        }
        options = options + "><label style=\"padding-left:5px; width:90%; font-weight:normal;\">" + result['optionA'] + "</label></div>";
        }

        if(result['optionB'] != "") {
          options = options + "<div class=\"form-group radio-pink-gap\">";
          options = options + "<input type=\"checkbox\" name=\"option\" class=\"with-gap\" style=\"vertical-align:top\"";
        if(result['isOptionB']) {
          options = options + "checked = \"checked\" ";
        }
        options = options + "><label style=\"padding-left:5px; width:90%; font-weight:normal;\">" + result['optionB'] + "</label></div>";
        }

        if(result['optionC'] != "") {
          options = options + "<div class=\"form-group radio-pink-gap\">";
          options = options + "<input type=\"checkbox\" name=\"option\" class=\"with-gap\" style=\"vertical-align:top\"";
        if(result['isOptionC']) {
          options = options + "checked = \"checked\" ";
        }
        options = options + "><label style=\"padding-left:5px; width:90%; font-weight:normal;\">" + result['optionC'] + "</label></div>";
        }

        if(result['optionD'] != "") {
          options = options + "<div class=\"form-group radio-pink-gap\">";
          options = options + "<input type=\"checkbox\" name=\"option\" class=\"with-gap\" style=\"vertical-align:top\"";
        if(result['isOptionD']) {
          options = options + "checked = \"checked\" ";
        }
        options = options + "><label style=\"padding-left:5px; width:90%; font-weight:normal;\">" + result['optionD'] + "</label></div>";
        }

        if(result['optionE'] != "") {
          options = options + "<div class=\"form-group radio-pink-gap\">";
          options = options + "<input type=\"checkbox\" name=\"option\" class=\"with-gap\" style=\"vertical-align:top\"";
        if(result['isOptionE']) {
          options = options + "checked = \"checked\" ";
        }
        options = options + "><label style=\"padding-left:5px; width:90%; font-weight:normal;\">" + result['optionE'] + "</label></div>";
        }
    }
    $('#subqns').html(qstring + options);
}
