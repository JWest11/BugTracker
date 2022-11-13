$(document).ready(function() {
    "use strict";

    /*======== 20. BAR CHART ========*/



var barX = document.getElementById("projectBarChart");
if (barX !== null) {

  let projectBarData = JSON.parse(document.getElementById('projectBarData').innerText);
  console.log(projectBarData)
  let barLabels = []
  let barData = []
  for (let key in projectBarData) {
    let label = key.split(" ")
    barLabels.push(label)
    barData.push(projectBarData[key])
  };
  var myChart = new Chart(barX, {
    type: "bar",
    data: {
      labels: barLabels,
      datasets: [
        {
          label: "tickets",
          data: barData,
          // data: [2, 3.2, 1.8, 2.1, 1.5, 3.5, 4, 2.3, 2.9, 4.5, 1.8, 3.4, 2.8],
          backgroundColor: "#4c84ff"
        }
      ]
    },
    options: {
      responsive: true,
      aspectRatio: 2.3/1,
      legend: {
        display: false
      },
      scales: {
        xAxes: [
          {
            gridLines: {
              drawBorder: false,
              display: false
            },
            ticks: {
              display: true, // hide main x-axis line
              beginAtZero: true
            },
            barPercentage: 1.8,
            categoryPercentage: 0.2
          }
        ],
        yAxes: [
          {
            gridLines: {
              drawBorder: false, // hide main y-axis line
              display: true
            },
            ticks: {
              display: true,
              beginAtZero: true,
              stepSize:1
            }
          }
        ]
      },
      tooltips: {
        titleFontColor: "#888",
        bodyFontColor: "#555",
        titleFontSize: 12,
        bodyFontSize: 15,
        backgroundColor: "rgba(256,256,256,0.95)",
        displayColors: false,
        borderColor: "rgba(220, 220, 220, 0.9)",
        borderWidth: 5
      }
    }
  });
};


var barX = document.getElementById("projectBarChart2");
if (barX !== null) {

  let projectBarData = JSON.parse(document.getElementById('projectBarData2').innerText);
  console.log(projectBarData)
  let barLabels = []
  let barData = []
  for (let key in projectBarData) {
    let label = key.split(" ")
    barLabels.push(label)
    barData.push(projectBarData[key])
  };
  var myChart = new Chart(barX, {
    type: "bar",
    data: {
      labels: barLabels,
      datasets: [
        {
          label: "members",
          data: barData,
          // data: [2, 3.2, 1.8, 2.1, 1.5, 3.5, 4, 2.3, 2.9, 4.5, 1.8, 3.4, 2.8],
          backgroundColor: "#4c84ff"
        }
      ]
    },
    options: {
      responsive: true,
      aspectRatio: 2.3/1,
      legend: {
        display: false
      },
      scales: {
        xAxes: [
          {
            gridLines: {
              drawBorder: false,
              display: false
            },
            ticks: {
              display: true, // hide main x-axis line
              beginAtZero: true
            },
            barPercentage: 1.8,
            categoryPercentage: 0.2
          }
        ],
        yAxes: [
          {
            gridLines: {
              drawBorder: false, // hide main y-axis line
              display: true
            },
            ticks: {
              display: true,
              beginAtZero: true,
              stepSize:1
            }
          }
        ]
      },
      tooltips: {
        titleFontColor: "#888",
        bodyFontColor: "#555",
        titleFontSize: 12,
        bodyFontSize: 15,
        backgroundColor: "rgba(256,256,256,0.95)",
        displayColors: false,
        borderColor: "rgba(220, 220, 220, 0.9)",
        borderWidth: 5
      }
    }
  });
};

/*======== 11. DOUGHNUT CHART ========*/
var doughnut = document.getElementById("projectTicketChart");
if (doughnut !== null) {
  var myDoughnutChart = new Chart(doughnut, {
    type: "doughnut",
    data: {
      labels: ["High Priority", "Medium Priority", "Low Priority", "None"],
      datasets: [
        {
          label: ["High Priority", "Medium Priority", "Low Priority", "None"],
          data: JSON.parse(document.getElementById("donutData").innerText),
          backgroundColor: ["#ff2828", "#f7f443", "#4cff5b", "#858585"],
          borderWidth: 1
          // borderColor: ['#4c84ff','#29cc97','#8061ef','#fec402']
          // hoverBorderColor: ['#4c84ff', '#29cc97', '#8061ef', '#fec402']
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      legend: {
        display: false
      },
      cutoutPercentage: 75,
      tooltips: {
        callbacks: {
          title: function(tooltipItem, data) {
            return data["labels"][tooltipItem[0]["index"]];
          },
          label: function(tooltipItem, data) {
            return data["datasets"][0]["data"][tooltipItem["index"]];
          }
        },
        titleFontColor: "#888",
        bodyFontColor: "#555",
        titleFontSize: 12,
        bodyFontSize: 14,
        backgroundColor: "rgba(256,256,256,0.95)",
        displayColors: true,
        borderColor: "rgba(220, 220, 220, 0.9)",
        borderWidth: 2
      }
    }
  });
};

});