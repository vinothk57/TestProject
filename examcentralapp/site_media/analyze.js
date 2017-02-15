graphdata = [
    ['Section', 'Mark'],
    ['2014', 1000],
    ['2015', 1170],
    ['2016', 60],
    ['2017', 130]

];


function success(gdata) {

  graphdata = [
     ['Section', 'Mark'],
     ['Unanswered', gdata['unanswered']],
     ['Correct Answers', gdata['correctanswers']],
     ['Wrong Answers', gdata['wronganswers']],
  ];
  var data = google.visualization.arrayToDataTable(graphdata);

  var options = {
    pieHole: 0.4,
    height: 400
  };

  var chart = new google.visualization.PieChart(document.getElementById('content-div'));

  chart.draw(data, options);
}

function drawChart() {
  var examidval = $("#examid").val();
  var attemptidval = $("#attemptid").val();
  $.getJSON("/getgraphdata/?ajax&examid=" + encodeURIComponent(examidval) + "&attemptid=" + encodeURIComponent(attemptidval), "", success);

}

$(document).ready(function () {
  google.charts.load('current', {'packages':['corechart']});
  google.charts.setOnLoadCallback(drawChart);

  //drawChart();
});
