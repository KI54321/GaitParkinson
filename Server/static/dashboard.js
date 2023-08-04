const firebaseConfig = {
  apiKey: "AIzaSyC4m-Zmkp828QJLXzRFsqe0taqW_DfAaB8",
  authDomain: "gait-76343.firebaseapp.com",
  projectId: "gait-76343",
  storageBucket: "gait-76343.appspot.com",
  messagingSenderId: "368210206582",
  appId: "1:368210206582:web:7f2a46d4a5613725dbe457",
  measurementId: "G-T51VMHB2N1",
};

const app = firebase.initializeApp(firebaseConfig);
const db = firebase.firestore();

let allData = [];
var currentChart = undefined;
var currentForceChart = undefined;
document.getElementById("gaitPickerDate").value =
  new Date().toLocaleDateString();
document.getElementById("forcePickerDate").value =
  new Date().toLocaleDateString();
$("#gaitPickerDate").datepicker({
  language: "en", // English language
  minDate: new Date(), // Start at today's date
  onSelect: function (form, date, inst) {
    addDatesData(date);
  },
  inline: false,
});
$("#forcePickerDate").datepicker({
  language: "en", // English language
  minDate: new Date(), // Start at today's date
  onSelect: function (form, date, inst) {
    addForceData(date);
  },
  inline: false,
});
db.collection("data")
  .orderBy("time", "desc")
  .get()
  .then(function (result) {
    console.log(result.docs);

    document.getElementById("updatedDateID").innerHTML = result.docs[0]
      .data()
      .time.toDate()
      .toLocaleTimeString("en-us", {
        month: "long",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });

    document.getElementById("dataEntries").innerHTML = String(
      result.docs.length
    );
    allData = result.docs;
    addDatesData(new Date());
    addForceData(new Date());
  });

function setUpCurrentDayMonitoring(data, labels) {
  var ctx2 = document.getElementById("chart-line").getContext("2d");

  var gradientStroke1 = ctx2.createLinearGradient(0, 230, 0, 50);

  gradientStroke1.addColorStop(1, "rgba(203,12,159,0.2)");
  gradientStroke1.addColorStop(0.2, "rgba(72,72,176,0.0)");
  gradientStroke1.addColorStop(0, "rgba(203,12,159,0)"); //purple colors

  var gradientStroke2 = ctx2.createLinearGradient(0, 230, 0, 50);

  gradientStroke2.addColorStop(1, "rgba(20,23,39,0.2)");
  gradientStroke2.addColorStop(0.2, "rgba(72,72,176,0.0)");
  gradientStroke2.addColorStop(0, "rgba(20,23,39,0)"); //purple colors

  if (currentChart != undefined) {
    currentChart.destroy();
  }
  currentChart = new Chart(ctx2, {
    type: "line",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Parkinsons",
          tension: 0.4,
          borderWidth: 0,
          pointRadius: 0,
          borderColor: "#cb0c9f",
          borderWidth: 3,
          backgroundColor: gradientStroke1,
          fill: true,
          data: data,
          maxBarThickness: 6,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false,
        },
      },
      interaction: {
        intersect: false,
        mode: "index",
      },
      scales: {
        y: {
          grid: {
            drawBorder: false,
            display: true,
            drawOnChartArea: true,
            drawTicks: false,
            borderDash: [5, 5],
          },
          ticks: {
            display: true,
            padding: 10,
            color: "#b2b9bf",
            font: {
              size: 11,
              family: "Open Sans",
              style: "normal",
              lineHeight: 2,
            },
          },
        },
        x: {
          grid: {
            drawBorder: false,
            display: false,
            drawOnChartArea: false,
            drawTicks: false,
            borderDash: [5, 5],
          },
          ticks: {
            display: true,
            color: "#b2b9bf",
            padding: 20,
            font: {
              size: 11,
              family: "Open Sans",
              style: "normal",
              lineHeight: 2,
            },
          },
        },
      },
    },
  });
}
function setUpCurrentForceMonitoring(leftData, rightData, labels) {
  var ctx2 = document.getElementById("forceChartID").getContext("2d");

  var gradientStroke1 = ctx2.createLinearGradient(0, 230, 0, 50);

  gradientStroke1.addColorStop(1, "rgba(203,12,159,0.2)");
  gradientStroke1.addColorStop(0.2, "rgba(72,72,176,0.0)");
  gradientStroke1.addColorStop(0, "rgba(203,12,159,0)"); //purple colors

  var gradientStroke2 = ctx2.createLinearGradient(0, 230, 0, 50);

  gradientStroke2.addColorStop(1, "rgba(20,23,39,0.2)");
  gradientStroke2.addColorStop(0.2, "rgba(72,72,176,0.0)");
  gradientStroke2.addColorStop(0, "rgba(20,23,39,0)"); //purple colors

  if (currentForceChart != undefined) {
    currentForceChart.destroy();
  }
  currentForceChart = new Chart(ctx2, {
    type: "line",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Left Force",
          tension: 0.4,
          borderWidth: 0,
          pointRadius: 0,
          borderColor: "#1a8cb8",
          borderWidth: 3,
          backgroundColor: gradientStroke1,
          fill: true,
          data: leftData,
          maxBarThickness: 6,
        },
        {
          label: "Right Force",
          tension: 0.4,
          borderWidth: 0,
          pointRadius: 0,
          borderColor: "#ce2525",
          borderWidth: 3,
          backgroundColor: gradientStroke2,
          fill: true,
          data: rightData,
          maxBarThickness: 6,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false,
        },
      },
      interaction: {
        intersect: false,
        mode: "index",
      },
      scales: {
        y: {
          grid: {
            drawBorder: false,
            display: true,
            drawOnChartArea: true,
            drawTicks: false,
            borderDash: [5, 5],
          },
          ticks: {
            display: true,
            padding: 10,
            color: "#b2b9bf",
            font: {
              size: 11,
              family: "Open Sans",
              style: "normal",
              lineHeight: 2,
            },
          },
        },
        x: {
          grid: {
            drawBorder: false,
            display: false,
            drawOnChartArea: false,
            drawTicks: false,
            borderDash: [5, 5],
          },
          ticks: {
            display: true,
            color: "#b2b9bf",
            padding: 20,
            font: {
              size: 11,
              family: "Open Sans",
              style: "normal",
              lineHeight: 2,
            },
          },
        },
      },
    },
  });
}
function sameDay(date1, date2) {
  return (
    date1.getFullYear() === date2.getFullYear() &&
    date1.getMonth() === date2.getMonth() &&
    date1.getDate() === date2.getDate()
  );
}
function addDatesData(date) {
  var todaysGaitPredictions = [];

  for (var i = allData.length - 1; i >= 0; i--) {
    if (sameDay(date, allData[i].data().time.toDate())) {
      todaysGaitPredictions.push(allData[i].data());
    }
  }
  setUpCurrentDayMonitoring(
    todaysGaitPredictions.map(function (oneData) {
      return oneData.class;
    }),
    todaysGaitPredictions.map(function (oneData) {
      return oneData.time.toDate().toLocaleTimeString("en-us", {
        hour: "2-digit",
        minute: "2-digit",
      });
    })
  );
}
function addForceData(date) {
  var leftForceData = [];
  var rightForceData = [];
  var timeData = [];
  for (var i = allData.length - 1; i >= 0; i--) {
    if (sameDay(date, allData[i].data().time.toDate())) {
      leftForceData.push(allData[i].data().TotalVGRFL);
      rightForceData.push(allData[i].data().TotalVGRFR);
      timeData.push(
        allData[i].data().time.toDate().toLocaleTimeString("en-us", {
          hour: "2-digit",
          minute: "2-digit",
        })
      );
    }
  }
  setUpCurrentForceMonitoring(leftForceData, rightForceData, timeData);
}
