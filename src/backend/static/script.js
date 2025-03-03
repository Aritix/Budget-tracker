document.addEventListener('DOMContentLoaded', () => {
    const mainUploadZone = document.getElementById('mainUploadZone');
    const mainFileUploader = document.getElementById('mainFile');
    const selectMainFileButton = document.getElementById('selectMainFileButton');
    const graphDisplayArea = document.getElementById('graphDisplayArea');
    const loadingState = document.getElementById('loadingState');
    const graphContainer = document.getElementById('graphContainer');
    const chartTypeSelect = document.getElementById('chartType');
    const referenceUploadZone = document.getElementById('referenceUploadZone');
    const referenceFileUploader = document.getElementById('referenceFile');
    const selectReferenceFileButton = document.getElementById('selectReferenceFileButton');
    const referenceFileNameDisplay = document.getElementById('referenceFileName');
    const exportButton = document.getElementById('exportButton'); // Added export button

    let referenceFile = null;

    function showLoading() {
        loadingState.classList.add('active');
        graphContainer.innerHTML = '';
    }

    function hideLoading() {
        loadingState.classList.remove('active');
    }

    chartTypeSelect.addEventListener('change', (event) => {
        const selectedChartType = event.target.value;
        console.log('Chart type selected:', selectedChartType);
    });

    selectReferenceFileButton.addEventListener('click', () => {
        referenceFileUploader.click();
    });

    referenceFileUploader.addEventListener('change', (event) => {
        referenceFile = event.target.files[0];
        if (referenceFile) {
            referenceFileNameDisplay.textContent = referenceFile.name;
            console.log('Reference file selected:', referenceFile.name);
        } else {
            referenceFileNameDisplay.textContent = 'No file selected';
            referenceFile = null;
        }
    });

    selectMainFileButton.addEventListener('click', () => {
        mainFileUploader.click();
    });

    mainFileUploader.addEventListener('change', (event) => {
        const files = Array.from(event.target.files); // Get FileList as an Array
        if (files && files.length > 0) {
            handleMainFiles(files); // Handle multiple files
        }
    });

    mainUploadZone.addEventListener('dragover', (event) => {
        event.preventDefault();
        mainUploadZone.classList.add('dragover');
    });

    mainUploadZone.addEventListener('dragleave', () => {
        mainUploadZone.classList.remove('dragover');
    });

    mainUploadZone.addEventListener('drop', (event) => {
        event.preventDefault();
        mainUploadZone.classList.remove('dragover');
        const files = Array.from(event.dataTransfer.files); // Get FileList as an Array
        if (files && files.length > 0) {
            handleMainFiles(files); // Handle multiple files
        }
    });

    // Export Button Click Event
    exportButton.addEventListener('click', () => {
        console.log('Export button clicked');
        // Future: Implement export functionality here
        alert('Export functionality will be implemented in future versions. Currently, this is a placeholder.'); // Placeholder alert
    });


    function handleMainFiles(files) { // Modified to handle multiple files
        console.log('Main data files uploaded:');
        files.forEach(file => console.log(file.name)); // Log each file name
        showLoading();

        setTimeout(() => {
            hideLoading();
            graphContainer.innerHTML = '<p class="placeholder-text">Graphs will be displayed here after graph generation is implemented for multiple files.</p>';
            console.log('Selected Chart Type for graph generation:', chartTypeSelect.value);
            if (referenceFile) {
                console.log('Reference File also considered:', referenceFile.name);
            }
        }, 1500);
    }


    referenceUploadZone.addEventListener('dragover', (event) => {
        event.preventDefault();
        referenceUploadZone.classList.add('dragover');
    });

    referenceUploadZone.addEventListener('dragleave', () => {
        referenceUploadZone.classList.remove('dragover');
    });

    referenceUploadZone.addEventListener('drop', (event) => {
        event.preventDefault();
        referenceUploadZone.classList.remove('dragover');
        referenceFile = event.dataTransfer.files[0];
        if (referenceFile) {
            referenceFileNameDisplay.textContent = referenceFile.name;
            console.log('Reference file uploaded via drag and drop:', referenceFile.name);
        }
    });
});