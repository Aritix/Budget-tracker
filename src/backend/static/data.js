// script.js
color_palette = ['#005f73', '#0081a7', '#00b4d8', '#90e0ef', '#48cae4', '#b5838d', '#a3b18a', '#6d6875', '#555b4c', '#2b2d42', '#370617', '#6a040f']
document.addEventListener('DOMContentLoaded', () => {
      // Initilisation data
      // categorie_names_list = getMetaData();
    async function init() {
      // const meta_data = await getMetaData()
      // const categorie_names_list = JSON.parse(meta_data.categories);
      // const months_list = JSON.parse(meta_data.months);
      const data = await getFilteredData(['*'], ['*']);
      // Example data (hardcoded for demonstration)
      const timeSeriesData = {
          labels: data.months,
          datasets: [{
              label: 'Total Expenses Over Time',
              data: data.month_sums,
              borderColor: 'rgb(75, 192, 192)',
              tension: 0.1,
              backgroundColor: color_palette
          }]
      };

      const pieChartData = {
          labels: data.categories,
          datasets: [{
              label: 'Expenses by Category',
              data: data.sums,
              backgroundColor: color_palette,
              hoverOffset: 4
          }]
      };
    
      // Get chart contexts
      const timeSeriesCtx = document.getElementById('timeSeriesChart').getContext('2d');
      const pieChartCtx = document.getElementById('pieChart').getContext('2d');

      // Create charts
      const timeSeriesChart = new Chart(timeSeriesCtx, {
          type: 'bar',
          data: timeSeriesData,
          options: {
              responsive: true,
              maintainAspectRatio: false,
              scales: {
                  y: {
                      beginAtZero: true
                  }
              }
          }
      });

      const pieChart = new Chart(pieChartCtx, {
          type: 'pie',
          data: pieChartData,
          options: {
              responsive: true,
              maintainAspectRatio: false
          }
      });
      const availableCategories = data.categories;
      const availableMonths = data.months;
  
      const categoryFiltersContainer = document.getElementById('category-filters');
      const monthFiltersContainer = document.getElementById('month-filters');
      function createFilterButtons(filters, container, filterType) {
          filters.forEach(filterName => {
              const button = document.createElement('button');
              button.classList.toggle('active'); // Initially active
              button.textContent = filterName;
              button.dataset.filterValue = filterName; // Store filter value
              button.dataset.filterType = filterType; // Store filter type
              button.addEventListener('click', handleFilterButtonClick);
              container.appendChild(button);
          });
      }
  
      createFilterButtons(availableCategories, categoryFiltersContainer, 'category');
      createFilterButtons(availableMonths, monthFiltersContainer, 'month');
      function handleFilterButtonClick(event) {
          const button = event.target;
          button.classList.toggle('active'); // Toggle active class for visual feedback
  
          // --- Simulate Data Filtering and Chart Update (Replace with Backend Fetch in Real App) ---
          const selectedCategories = Array.from(categoryFiltersContainer.querySelectorAll('button.active'))
              .map(btn => btn.dataset.filterValue);
          const selectedMonths = Array.from(monthFiltersContainer.querySelectorAll('button.active'))
              .map(btn => btn.dataset.filterValue);
  
          console.log('Selected Categories:', selectedCategories);
          console.log('Selected Months:', selectedMonths);
  
          // --- In a real application, you would: ---
          // 1. Construct an API request to your backend with selected filters.
          // 2. Use fetch() to get filtered data from the backend.
          // 3. Process the data received from the backend.
          // 4. Update the chart data and re-render the charts.
          updateChartsWithFilteredData(selectedCategories, selectedMonths); // Simulate update
      }
  
  
      // --- Function to Simulate Chart Update with Filtered Data ---
      async function updateChartsWithFilteredData(selectedCategories, selectedMonths) {
          console.log('Chart update with filters:', selectedCategories, selectedMonths);
          const data = await getFilteredData(selectedCategories, selectedMonths)
          const categories = data.categories;
          const categorie_sums = data.categorie_sums;
          const months = data.categorie_sums;
          const  month_sums = data.month_sums;
          pieChart.data.datasets[0].data = categorie_sums;
          pieChart.data.labels = categories;
          pieChart.update();
          timeSeriesChart.data.datasets[0].data = month_sums;
          timeSeriesChart.data.labels = months;
          timeSeriesChart.update();
      }
    }
    // Function to handle filter button clicks

    async function getMetaData() {
        const response = await fetch('/getMetaData');
        const data = await response.json();
        return data;
      }
      
      async function getFilteredData(selectedCategories, selectedMonths) {
        const url = '/getFilteredData';
        try {
          const response = await fetch(url, { method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ time_filter:  selectedCategories, category_filter: selectedMonths })});
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          json = await response.json();
          console.log('Filtered data : ', json);
          const categories_data = JSON.parse(json.categories);
          const months_data = JSON.parse(json.months);
          const categories = Object.keys(categories_data);
          const categorie_sums = categories.map(category => categories_data[category]);
          const months = Object.keys(months_data);
          const month_sums = months.map(month => months_data[month]);
          return { categories: categories, categorie_sums: categorie_sums , months : months, month_sums : month_sums};
        } catch (error) {
          console.error('Error fetching or parsing data:', error);
          return { categories: [], sums: [] , categorie_sums : [], months, month_sums : []};
        }
      }
      init();
    });