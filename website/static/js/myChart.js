var ctx = document.getElementById("chart").getContext("2d");

var options = {
  legendTemplate : "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<datasets.length; i++){%><li><span style=\"background-color:<%=datasets[i].strokeColor%>\"></span><%if(datasets[i].label){%><%=datasets[i].label%><%}%></li><%}%></ul>"
}

var data = {
  labels: ["Avg Tax", "Avg Medicare Levy", "Avg HELP Debt"],
  datasets: [
    {
      label: "Suburb",
      fillColor: "rgba(220,220,220,0.5)",
      strokeColor: "rgba(220,220,220,0.8)",
      highlightFill: "rgba(220,220,220,0.75)",
      highlightStroke: "rgba(220,220,220,1)",
      data: [sub_tax, sub_medi, sub_hex]
    },
    {
      label: "Average",
      fillColor: "rgba(151,187,205,0.5)",
      strokeColor: "rgba(151,187,205,0.8)",
      highlightFill: "rgba(151,187,205,0.75)",
      highlightStroke: "rgba(151,187,205,1)",
      data: [13780, 890, 146]
    }
  ]
};

var barChart = new Chart(ctx).Bar(data, options);
