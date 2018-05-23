var currqtnno = 1;
var lastqtnno = 1;
var totalqtn = $("#totalqtns").val();
var loadQuestionAt = "#langList";
var loadQInfoAt = "#langqtninfo";
var getLastQtn = false;
var JSONAnswerData = {};
JSONAnswerData['ansList'] = {};

//Model JSON
var JSONObj = {
};

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function showCorrectTab() {

  var loadqtn = true;
      if(JSONObj['qlist'][currqtnno - 1]['qcategory'] == "4") {
        $('.nav-tabs a[href="#general"]').tab('show');
        if(loadQuestionAt != "#genList") {
          loadQuestionAt = "#genList";
          loadQInfoAt = "#genqtninfo";
          loadqtn = false;
        }
      } else if(JSONObj['qlist'][currqtnno - 1]['qcategory'] == "2") {
        $('.nav-tabs a[href="#analysis"]').tab('show');
        if(loadQuestionAt != "#analysisList") {
          loadQuestionAt = "#analysisList";
          loadQInfoAt = "#analysisqtninfo";
          loadqtn = false;
        }
      } else if(JSONObj['qlist'][currqtnno - 1]['qcategory'] == "1") {
        $('.nav-tabs a[href="#language"]').tab('show');
        if(loadQuestionAt != "#langList") {
          loadQuestionAt = "#langList";
          loadQInfoAt = "#langqtninfo";
          loadqtn = false;
        }
      } else if(JSONObj['qlist'][currqtnno - 1]['qcategory'] == "3") {
        $('.nav-tabs a[href="#reasoning"]').tab('show');
        if(loadQuestionAt != "#reasonList") {
          loadQuestionAt = "#reasonList";
          loadQInfoAt = "#reasoningqtninfo";
          loadqtn = false;
        }
      }

   if(loadqtn) {
      loadQuestionData();
   }
}

function saveAnswer() {
  var ans = "";
  var i = 1;
  $(loadQuestionAt + " :input").each(function () {
      if(this.checked) {
        ans = ans + i + " ";
        JSONObj['qlist'][currqtnno - 1]['options'][i -1]['checked'] = "true";
      } else {
        JSONObj['qlist'][currqtnno - 1]['options'][i -1]['checked'] = "false";
      }
      i++;
  });
  // "this" is the current element in the loop
  var qid = "qno" + currqtnno;
  $('#' + qid).removeClass("notvisit-btn markrew-btn"); 
  if(ans != "") {
    $('#' + qid).removeClass("notans-btn"); 
    $('#' + qid).addClass("ans-btn");
  } else {
    $('#' + qid).removeClass("ans-btn"); 
    $('#' + qid).addClass("notans-btn");
  }

  if(ans != "") {
    JSONAnswerData['ansList'][currqtnno] = ans;
  } else {
    if (currqtnno in JSONAnswerData['ansList']) {
      delete JSONAnswerData['ansList'][currqtnno]
    }
  }
}

function checkAnswered() {
  var ans = "";
  var i = 1;
  $(loadQuestionAt + ' :input').each(function () {
      if(this.checked) {
        ans = ans + i + " ";
        JSONObj['qlist'][currqtnno - 1]['options'][i -1]['checked'] = "true";
      } else {
        JSONObj['qlist'][currqtnno - 1]['options'][i -1]['checked'] = "false";
      }
      i++;
  });
  // "this" is the current element in the loop
  var qid = "qno" + currqtnno;
  if ( $('#' + qid).hasClass('markrew-btn')) {
  } else {
    $('#' + qid).removeClass("notvisit-btn markrew-btn");
    if(ans != "") {
      $('#' + qid).removeClass("notans-btn");
      $('#' + qid).addClass("ans-btn");
    } else {
      $('#' + qid).removeClass("ans-btn");
      $('#' + qid).addClass("notans-btn");
    }
  }

  if(ans != "") {
    JSONAnswerData['ansList'][currqtnno] = ans;
  } else {
    if (currqtnno in JSONAnswerData['ansList']) {
      delete JSONAnswerData['ansList'][currqtnno]
    }
  }
}

function getLastQtnOfCategory(category) {
  var qtnFound = false;
  for (i = JSONObj['qlist'].length -1; i >=0; i--) {
    var qno = i + 1;
    if(JSONObj['qlist'][i]['qcategory'] == category) {
       currqtnno = qno;
       qtnFound = true;
       break;
    }
  }
  if( qtnFound == true) {
    loadQuestionData();
    showCorrectBtns();
  }
  return false;
}

function getFirstQtnOfCategory(category) {
  var qtnFound = false;
  for (i = 0; i <  JSONObj['qlist'].length; i++) {
    var qno = i + 1;
    if(JSONObj['qlist'][i]['qcategory'] == category) {
       currqtnno = qno;
       qtnFound = true;
       break;
    }
  }
  if( qtnFound == true) {
    loadQuestionData();
    showCorrectBtns();
  }
  return false;
}

function showQuestionsOfCategory(category) {
    for (i = 0; i <  JSONObj['qlist'].length; i++) {
      var qno = i + 1;
      if(JSONObj['qlist'][i]['qcategory'] != category) {
         $("#qno" + qno).hide();
      } else {
         $("#qno" + qno).show();
      }
    }
    if(category == "4") {
      loadQuestionAt = "#genList";
      loadQInfoAt = "#genqtninfo";
    } else if(category == "2") {
      loadQuestionAt = "#analysisList";
      loadQInfoAt = "#analysisqtninfo";
    } else if(category == "1") {
      loadQuestionAt = "#langList";
      loadQInfoAt = "#langqtninfo";
    } else if(category == "3") {
      loadQuestionAt = "#reasonList";
      loadQInfoAt = "#reasoningqtninfo";
    }

    if(getLastQtn == true) {
      getLastQtnOfCategory(category);
    } else {
      getFirstQtnOfCategory(category);
    }
}

function getqtnfromJSON() {
  var examid = $("#examid").val();
  var qno = $("input[type=submit][clicked=true]").val();
  checkAnswered();
  lastqtnno = currqtnno;
  currqtnno = qno;

  //var qelement = JSONObj['qlist'][currqtnno - 1];
  //var qstring = "<p><strong>" + qelement['qno'] + ". " + qelement['qtn'] + "</strong></p>";

  //var options = "";
  //if(qelement['type'] == 1) {
  //  for (i = 0; i <  qelement['options'].length; i++) {
  //    options = options + "<br><input type=\"radio\" name=\"option\" ";
  //    if(qelement['options'][i]['checked'] == "true") {
  //      options = options + "checked = \"checked\" ";
  //    }
  //    options = options + "/>" + qelement['options'][i]['option'];
  //  }
  //} else if (qelement['type'] == 2) {
  //  for (i = 0; i <  qelement['options'].length; i++) {
  //    options = options + "<br><input type=\"checkbox\" name=\"option\" ";
  //    if(qelement['options'][i]['checked'] == "true") {
  //      options = options + "checked = \"checked\" ";
  //    }
  //    options = options + "/>" + qelement['options'][i]['option'];
  //  }
  //}

  //$("#myList").html(
  //  qstring + options
  //);
  loadQuestionData();
  showCorrectBtns();
  return false;
}
//End
function getqtn_submit() { 
  var examid = $("#examid").val();
  var qno = $("input[type=submit][clicked=true]").val();
  currqtnno = qno;

  var query_string = "/getqtn/?ajax&examid=" + encodeURIComponent(examid) + "&qid=" + qno
 
  $(loadQuestionAt).load(
    query_string 
  );
  showCorrectBtns();
  return false;
}

function loadQuestionData() {
    var qelement = JSONObj['qlist'][currqtnno - 1];
    var qstring = "<h6><pre style=\"white-space: pre-wrap;word-wrap: break-word;white-space: -o-pre-wrap;white-space: -moz-pre-wrap;\">" + qelement['qno'] + ". " + qelement['qtn'] + "</pre></h6>";

    var options = "";
    if(qelement['type'] == 1) {
      for (i = 0; i <  qelement['options'].length; i++) {
        options = options + "<div class=\"form-group radio-pink-gap\">";
        options = options + "<input type=\"radio\" name=\"option\" class=\"with-gap\" style=\"vertical-align:top\"";
        if(qelement['options'][i]['checked'] == "true") {
          options = options + "checked = \"checked\" ";
        }
        options = options + "><label style=\"padding-left:5px; width:90%; font-weight:normal;\">" + qelement['options'][i]['option'] + "</label></div>";
      }
    } else if (qelement['type'] == 3) {
      for (i = 0; i <  qelement['options'].length; i++) {
        options = options + "<div class=\"form-group radio-pink-gap\">";
        options = options + "<input type=\"checkbox\" name=\"option\" class=\"with-gap\" style=\"vertical-align:top\"";
        if(qelement['options'][i]['checked'] == "true") {
          options = options + "checked = \"checked\" ";
        }
        options = options + "><label style=\"padding-left:5px; width:90%; font-weight:normal;\">" + qelement['options'][i]['option'] + "</label></div>";
      }
    }

    $(loadQuestionAt).html(
      qstring + options
    );

    var addInfo = "";
    if ("direction" in qelement) {
        addInfo = "<h5 style=\"line-height: 21px; text-align: justify;\">" + qelement['direction'] + "</h5>";
    }
    if ("imgpath" in qelement) {
        addInfo += "<img src=" + qelement['imgpath'] + ">";
    }
    $(loadQInfoAt).html(addInfo);
}

function getnextqtnJSON() {
    var examid = $("#examid").val();
    currqtnno++;
    if(currqtnno <= Number(totalqtn)) {
      setTimeout(showCorrectTab(),100);
      //loadQuestionData();
    } else {
      currqtnno--;
    }
    showCorrectBtns();
    return false;
}

function getnextqtn() {
    var examid = $("#examid").val();
    currqtnno++;
    if(currqtnno <= Number(totalqtn)) {
      var qno = currqtnno;
      var query_string = "/getqtn/?ajax&examid=" + encodeURIComponent(examid) + "&qid=" + qno
      $(loadQuestionAt).load(
        query_string
      );
    } else {
      currqtnno--;
    }
    showCorrectBtns();
}

function showCorrectBtns() {
    if(currqtnno == Number(1)) {
      $("#prev").hide();
    }
    if(currqtnno > Number(1)) {
      $("#prev").show();
    } 
    if(currqtnno < Number(totalqtn)) {
      $("#review").prop('value', 'Mark for Review and Next');
      $("#next").prop('value', 'Save and Next');
    }
    if(currqtnno == Number(totalqtn)) {
      $("#review").prop('value', 'Mark for Review');
      $("#next").prop('value', 'Save');
    }
}

function success(data) {
  JSONObj = data;
  showQuestionsOfCategory(1);
  getFirstQtnOfCategory(1);
  //loadQuestionData();
  //showCorrectBtns();
}

function viewResult() {
  JSONdata = {};
  JSONdata['examid'] = $("#examid").val();
  JSONdata['attemptid'] = $("#attemptid").val();
  $.ajax({
         url: "/showresult/",
         type: "post",
         dataType: "json",
         data: {
               json: JSON.stringify(JSONdata)
         },
         success: function(result) {
             $("#content-div").html("<h4> Result </h4> \
                                     <table class=\"table table-striped\"> \
                                       <thead> \
                                         <tr> \
                                           <th>Item</th> \
                                           <th>Value</th> \
                                         </tr> \
                                       </thead> \
                                       <tbody> \
                                         <tr> \
                                           <td>Exam Name</td> \
                                           <td>" + result["examname"] + "</td> \
                                         </tr> \
                                         <tr> \
                                           <td>Attempt No.</td> \
                                           <td>" + result["attemptid"] + "</td> \
                                         </tr> \
                                         <tr> \
                                           <td>Start Time</td> \
                                           <td>" + result["start_time"] + "</td> \
                                         </tr> \
                                         <tr> \
                                           <td>End Time</td> \
                                           <td>" + result["end_time"] + "</td> \
                                         </tr> \
                                         <tr> \
                                           <td>Total Questions</td> \
                                           <td>" + result["totalqtns"] + "</td> \
                                         </tr> \
                                         <tr> \
                                           <td>Answered Questions</td> \
                                           <td>" + result["answered_questions"] + "</td> \
                                         </tr> \
                                         <tr> \
                                           <td>Correct Answers</td> \
                                           <td>" + result["correctly_answered"] + "</td> \
                                         </tr> \
                                         <tr> \
                                           <td>Total Score</td> \
                                           <td>" + result["mark"] + "</td> \
                                         </tr> \
                                       </tbody> \
                                     </table><br><br>");

         },
         error: function(data){
             alert('error; ' + JSON.stringify(data));
         }
  });
  return false;
}

$(document).ready(function () {

//  $("#getqtn-form").submit(getqtn_submit);
  var examidval = $("#examid").val();
  $.getJSON("/fetchpaper/?ajax&examid=" + encodeURIComponent(examidval), "", success);

  $("#getqtn-form").submit(getqtnfromJSON);

  $("form input[type=submit]").click(function() {
      $("input[type=submit]", $(this).parents("form")).removeAttr("clicked");
      $(this).attr("clicked", "true");
  });

  $("#next").click(function() {
    //getnextqtn();
    var qid = "qno" + currqtnno;
    $('#' + qid).removeClass("markrew-btn"); 
    saveAnswer();
    lastqtnno = currqtnno;
    getnextqtnJSON();
    return false;
  });

  $("#prev").click(function() {
    var examid = $("#examid").val();
    checkAnswered();
    lastqtnno = currqtnno;
    currqtnno--;
    if( currqtnno != Number("0")) {
      getLastQtn = true;
      showCorrectTab();
      //loadQuestionData();
      //var qno = currqtnno;
      //var query_string = "/getqtn/?ajax&examid=" + encodeURIComponent(examid) + "&qid=" + qno
      //$("#myList").load(
      //  query_string
      //);
    } else {
      currqtnno++;
    }
    showCorrectBtns();
    setTimeout(function() {getLastQtn = false;},1000);
    return false;
  });

  $("#clear").click(function() {
    $('input[type=checkbox]').each(function() 
    { 
            this.checked = false; 
    });
    $('input[type=radio]').each(function() 
    { 
            this.checked = false; 
    });
    
  });

  $("#review").click(function() {
    var qid = "qno" + currqtnno;
    lastqtnno = currqtnno;
    saveAnswer();
    $('#' + qid).removeClass("ans-btn notans-btn"); 
    $('#' + qid).addClass("markrew-btn"); 
    getnextqtnJSON();
    return false;
  });

  $('a[data-toggle="tab"]').on('shown.bs.tab', function(e) {
      var target = $(e.target).attr("href");
      var showcategory = 1;
      if(target == "#general") {
        showcategory = 4;
      } else if (target == "#analysis") {
        showcategory = 2;
      } else if (target == "#language") {
        showcategory = 1;
      } else if (target == "#reasoning") {
        showcategory = 3;
      }
      showQuestionsOfCategory(showcategory);
    }
  );

  $("#submitexam").click(function(e) {
     e.preventDefault();
     $("#countdown").hide();
     JSONAnswerData['examid'] = $("#examid").val();
     JSONAnswerData['attemptid'] = $("#attemptid").val();
     $.ajax({
         url: "/evaluateexam/",
         type: "post",
         dataType: "json",
         data: {
               json: JSON.stringify(JSONAnswerData),
               csrfmiddlewaretoken: csrftoken
         },
         success: function(result) {
/*             $("#content-div").html("<h4>Exam Submitted successfully</h4><br> \
                          <input type=\"hidden\" id=\"examid\" value=\"" + result["examid"] + "\" /> \
                          <input type=\"hidden\" id=\"attemptid\" value=\"" + result["attemptid"] + "\" /> \
                        <button type=\"button\" onclick=\"viewResult()\" class=\"exam-btn info\">View Result</button><br><br>");*/

             var form = $(document.createElement('form'));
             $(form).attr("action", "/analyzeexam/");
             $(form).attr("method", "POST");

             var input1 = $("<input>")
               .attr("type", "hidden")
               .attr("name", "examid")
               .val(result["examid"]);

             var input2 = $("<input>")
               .attr("type", "hidden")
               .attr("name", "attemptid")
               .val(result["attemptid"]);

             var input3 = $("<input>")
               .attr("type", "hidden")
               .attr("name", "csrfmiddlewaretoken")
               .val(csrftoken);

             $(form).append($(input1));
             $(form).append($(input2));
             $(form).append($(input3));
             form.appendTo( document.body )
             $(form).submit();

            $("#loading").hide();
            JSONObj = {};
         },
         error: function(data){
             alert('error; ' + JSON.stringify(data));
         }
     });
    return false;
  });

  var examid = $("#examid").val();
  var qno = currqtnno;
});
