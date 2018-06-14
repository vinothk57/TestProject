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
     ['Wrong Answers', gdata['wronganswers']],
     ['Correct Answers', gdata['correctanswers']],
  ];
  var data = google.visualization.arrayToDataTable(graphdata);

  var options = {
    pieHole: 0.5,
  };

  var chart = new google.visualization.PieChart(document.getElementById('content-div'));

  chart.draw(data, options);
}

function success_sectiondata(gdata) {

  var sectionchart = new google.visualization.ColumnChart(document.getElementById('sectionchart-div'));
  var sdata = new google.visualization.DataTable();
  sdata.addColumn('string', 'Section Name');
  sdata.addColumn('number', 'Total');
  sdata.addColumn('number', 'Answered');
  sdata.addColumn('number', 'Correctly Answered');

  for(var i =0; i < gdata['dataList'].length; i++)
    sdata.addRow(gdata['dataList'][i]);
  var soptions = {
    title: 'Section-wise performance',
    colors: ['#4575cd', '#ffd030', '#63ac71'],
    titleTextStyle: {
        color: "#d663c2",
        fontName: 'Arial',
        bold: false,
        fontSize: 22
    },
    hAxis: {
      title: 'Exam Sections',
      titleTextStyle: {
        color: "#1653c2",
        fontName: 'Arial',
        fontSize: 18
      },
      textStyle: {
        fontName: 'Arial',
        fontSize: 17
      }
    },
    vAxis: {
      title: 'Number of Questions',
      titleTextStyle: {
        color: "#1653c2",
        fontName: 'Arial',
        fontSize: 18
      },
      textStyle: {
        fontName: 'Arial',
        fontSize: 17
      }
    }
  };

  sectionchart.draw(sdata, soptions);
}

function drawChart() {
  var examidval = $("#examid").val();
  var attemptidval = $("#attemptid").val();
  $.getJSON("/getgraphdata/?ajax&examid=" + encodeURIComponent(examidval) + "&attemptid=" + encodeURIComponent(attemptidval), "", success);
  $.getJSON("/getsectiondata/?ajax&examid=" + encodeURIComponent(examidval) + "&attemptid=" + encodeURIComponent(attemptidval), "", success_sectiondata);
}

$(document).ready(function () {
  google.charts.load('current', {'packages':['corechart', 'bar']});
  google.charts.setOnLoadCallback(drawChart);

  //drawChart();
});
