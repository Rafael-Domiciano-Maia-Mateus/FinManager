const labels = JSON.parse(document.getElementById("labels-data").textContent);
const values = JSON.parse(document.getElementById("values-data").textContent);

const ctx = document.getElementById("expenseChart");

new Chart(ctx, {
  type: "bar",
  data: {
    labels: labels,
    datasets: [
      {
        label: "Expenses",
        data: values,
        borderWidth: 1,
      },
    ],
  },
  options: {
    responsive: true,
    animation: false,
    scales: {
      y: { beginAtZero: true },
    },
  },
});
