const labels = JSON.parse(document.getElementById("labels-data").textContent);
const values = JSON.parse(document.getElementById("values-data").textContent);

const ctx = document.getElementById("expenseChart");
const wrapper = document.querySelector(".chart-wrapper");

let chartInstance = null;

function createChart(type) {
  if (chartInstance) {
    chartInstance.destroy();
  }

  if (type === "pie") {
    wrapper.style.maxWidth = "380px";
    wrapper.style.height = "380px";
    wrapper.style.margin = "0 auto";
  } else {
    wrapper.style.maxWidth = "100%";
    wrapper.style.height = "420px";
  }

  chartInstance = new Chart(ctx, {
    type: type,
    data: {
      labels: labels,
      datasets: [
        {
          label: "Expenses",
          data: values,
          borderWidth: 2,
          fill: type === "line",
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: true,
      plugins: {
        datalabels:
          type === "pie"
            ? {
                color: "#fff",
                font: {
                  weight: "bold",
                  size: 14,
                },
                formatter: (value, context) => {
                  const total = context.chart.data.datasets[0].data.reduce((a, b) => a + b, 0);
                  const percentage = ((value / total) * 100).toFixed(1);
                  return percentage + "%";
                },
              }
            : false,
      },
      scales:
        type === "pie"
          ? {}
          : {
              y: {
                beginAtZero: true,
              },
            },
    },
    plugins: type === "pie" ? [ChartDataLabels] : [],
  });
}

createChart("bar");

document.querySelectorAll(".chart-controls button").forEach((btn) => {
  btn.addEventListener("click", () => {
    createChart(btn.dataset.type);
  });
});
