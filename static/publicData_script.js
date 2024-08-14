document.addEventListener("DOMContentLoaded", function() {
    const currentDateElement = document.getElementById('currentDate');
    const now = new Date();

    // Calculate the previous month
    const lastMonth  = new Date(now.getFullYear(), now.getMonth()-1);

    // Format dates as YYYYMM
    const formatDate = date => {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        return `${year}${month}`;
    };

    const print_lastMonth = formatDate(lastMonth);

    currentDateElement.textContent = `조회 가능 기간: 201501 ~ ${print_lastMonth}`;
});

$(document).ready(function() {
    $('#dataForm').on('submit', function(event) {
        event.preventDefault(); // 기본 폼 제출을 방지

        const date = $('#date').val();
        const time = $('#time').val();

        const requestData = {
            date: date,
            time: time
        };

        $.ajax({
            url: '/show_public-data',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(requestData),
            success: function(response) {
                console.log('Success:', response);
                renderTable(response.final_P1, '#tableContainer1', 'heading1');
                renderTable(response.final_P4, '#tableContainer2', 'heading2');
                addDownloadButtons(date); // 버튼 추가
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
            }
        });
    });

    function renderTable(data, containerSelector, headingId) {
        const container = $(containerSelector);
        const headingElement = document.getElementById(headingId);
        
        container.empty(); // 기존 내용 지우기

        if (headingElement) {
            headingElement.classList.remove('hidden'); // 제목 표시
        }

        if (!Array.isArray(data) || data.length === 0) {
            container.html('<p>No data available.</p>');
            return;
        }

        const table = $('<table></table>');
        const thead = $('<thead></thead>');
        const tbody = $('<tbody></tbody>');

        const headerRow = $('<tr></tr>');
        for (const key in data[0]) {
            headerRow.append($('<th></th>').text(key));
        }
        thead.append(headerRow);

        data.forEach(item => {
            const row = $('<tr></tr>');
            for (const key in item) {
                row.append($('<td></td>').text(item[key]));
            }
            tbody.append(row);
        });

        table.append(thead);
        table.append(tbody);
        container.append(table);
    }

    function addDownloadButtons(date) {
        console.log('addDownloadButtons 호출됨');

        const buttonContainer = document.getElementById('buttonContainer');
        buttonContainer.innerHTML = '';
        const containers = ['#tableContainer1', '#tableContainer2'];
        const buttonLabels = [
            '1호선 승하차 인원 \nCSV 다운로드',
            '4호선 승하차 인원 \nCSV 다운로드'
        ];
        const fileNames = [
            `Line1_PassengerCount_${date}.csv`,
            `Line4_PassengerCount_${date}.csv`
        ];

        containers.forEach((selector, index) => {
            const button = document.createElement('button');
            button.textContent = buttonLabels[index] || `Download CSV ${index + 1}`;
            button.addEventListener('click', () => {
                const table = document.querySelector(selector + ' table');
                const csvContent = generateCSVFromTable(table);
                downloadCSV(csvContent, fileNames[index] || `table_${index + 1}.csv`);
            });
            buttonContainer.appendChild(button);
        });
    }

    function generateCSVFromTable(table) {
        let csv = [];
        const rows = table.querySelectorAll('tr');

        rows.forEach(row => {
            const cells = row.querySelectorAll('th, td');
            const rowContent = [];
            cells.forEach(cell =>{
                rowContent.push(cell.textContent.trim());
            });
            csv.push(rowContent.join(','));
        });
        return csv.join('\n');
    }

    function downloadCSV(csvContent, filename) {
        const BOM = "\uFEFF";
        csvContent = BOM + csvContent;
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        const url = URL.createObjectURL(blob);
        if (link.download !== undefined) {
            link.setAttribute('href', url);
            link.setAttribute('download', filename);
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            window.URL.revokeObjectURL(url);
        }
    }
});
