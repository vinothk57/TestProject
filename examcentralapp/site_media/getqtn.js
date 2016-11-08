var currqtnno = 1;
var lastqtnno = 1;
var totalqtn = $("#totalqtns").val();
var loadQuestionAt = "#genList";
var getLastQtn = false;

//Model JSON
var JSONObj = {
};

function showCorrectTab() {

  var loadqtn = true;
      if(JSONObj['qlist'][currqtnno - 1]['qcategory'] == "1") {
        $('.nav-tabs a[href="#general"]').tab('show');
        if(loadQuestionAt != "#genList") {
          loadQuestionAt = "#genList";
          loadqtn = false;
        }
      } else if(JSONObj['qlist'][currqtnno - 1]['qcategory'] == "2") {
        $('.nav-tabs a[href="#analysis"]').tab('show');
        if(loadQuestionAt != "#analysisList") {
          loadQuestionAt = "#analysisList";
          loadqtn = false;
        }
      } else if(JSONObj['qlist'][currqtnno - 1]['qcategory'] == "3") {
        $('.nav-tabs a[href="#language"]').tab('show');
        if(loadQuestionAt != "#langList") {
          loadQuestionAt = "#langList";
          loadqtn = false;
        }
      } else if(JSONObj['qlist'][currqtnno - 1]['qcategory'] == "4") {
        $('.nav-tabs a[href="#reasoning"]').tab('show');
        if(loadQuestionAt != "#reasonList") {
          loadQuestionAt = "#reasonList";
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
  $(loadQuestionAt).children('input').each(function () {
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
  $('#' + qid).removeClass("notvstd-btn review-btn"); 
  if(ans != "") {
    $('#' + qid).removeClass("notans-btn"); 
    $('#' + qid).addClass("ansd-btn");
  } else {
    $('#' + qid).removeClass("ansd-btn"); 
    $('#' + qid).addClass("notans-btn");
  }
}

function checkAnswered() {
  var ans = "";
  var i = 1;
  $(loadQuestionAt).children('input').each(function () {
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
  if ( $('#' + qid).hasClass('review-btn')) {
  } else {
    $('#' + qid).removeClass("notvstd-btn review-btn");
    if(ans != "") {
      $('#' + qid).removeClass("notans-btn");
      $('#' + qid).addClass("ansd-btn");
    } else {
      $('#' + qid).removeClass("ansd-btn");
      $('#' + qid).addClass("notans-btn");
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
    if(category == "1") {
      loadQuestionAt = "#genList";
    } else if(category == "2") {
      loadQuestionAt = "#analysisList";
    } else if(category == "3") {
      loadQuestionAt = "#langList";
    } else if(category == "4") {
      loadQuestionAt = "#reasonList";
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
    var qstring = "<p><strong>" + qelement['qno'] + ". " + qelement['qtn'] + "</strong></p>";

    var options = "";
    if(qelement['type'] == 1) {
      for (i = 0; i <  qelement['options'].length; i++) {
        options = options + "<br><input type=\"radio\" name=\"option\" ";
        if(qelement['options'][i]['checked'] == "true") {
          options = options + "checked = \"checked\" ";
        }
        options = options + "/>" + qelement['options'][i]['option'];
      }
    } else if (qelement['type'] == 2) {
      for (i = 0; i <  qelement['options'].length; i++) {
        options = options + "<br><input type=\"checkbox\" name=\"option\" ";
        if(qelement['options'][i]['checked'] == "true") {
          options = options + "checked = \"checked\" ";
        }
        options = options + "/>" + qelement['options'][i]['option'];
      }
    }

    $(loadQuestionAt).html(
      qstring + options
    );
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
    $('#' + qid).removeClass("review-btn"); 
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
    $('#' + qid).removeClass("ansd-btn notans-btn"); 
    $('#' + qid).addClass("review-btn"); 
    getnextqtnJSON();
    return false;
  });

  $('a[data-toggle="tab"]').on('shown.bs.tab', function(e) {
      var target = $(e.target).attr("href");
      var showcategory = 1;
      if(target == "#general") {
        showcategory = 1;
      } else if (target == "#analysis") {
        showcategory = 2;
      } else if (target == "#language") {
        showcategory = 3;
      } else if (target == "reasoning") {
        showcategory = 4;
      }
      showQuestionsOfCategory(showcategory);
    }
  );

  $("#submitexam").click(function() {
     var JSONAnswerData = {};
     JSONAnswerData['examid'] = $("#examid").val();
     JSONAnswerData['ansList'] = [];
     $.ajax({
         url: '/evaluateexam',
         type: 'POST',
         data: {json: JSON.stringify(JSONAnswerData)}
     })
  });

  var examid = $("#examid").val();
  var qno = currqtnno;
});
