const ctx = document.getElementById("machineChart").getContext("2d");
const machineChart = new Chart(ctx, {
  type: "line",
  data: {
    labels: [],
    datasets: [
      {
        label: "Machine Data",
        data: [],
        borderColor: "rgba(75, 192, 192, 1)",
        borderWidth: 1,
      },
    ],
  },
  options: {
    scales: {
      x: { title: { display: true, text: "Timestamp" } },
      y: { title: { display: true, text: "Value" } },
    },
  },
});

const socket = new WebSocket("ws://technest.ddns.net:8001/ws");

socket.onmessage = function (event) {
  console.log("Received data:", event.data);
  const data = JSON.parse(event.data);
  const time = new Date(data.timestamp).toLocaleTimeString();
  const value = data.value;

  machineChart.data.labels.push(time);
  machineChart.data.datasets[0].data.push(value);

  if (machineChart.data.labels.length > 20) {
    machineChart.data.labels.shift();
    machineChart.data.datasets[0].data.shift();
  }

  machineChart.update();
};
