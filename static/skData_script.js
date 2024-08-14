document.addEventListener("DOMContentLoaded", function() {
    const currentDateElement = document.getElementById('currentDate');
    if (currentDateElement) {
        const now = new Date();
        const startDate = new Date(now);
        startDate.setDate(startDate.getDate() - 29);

        const endDate = new Date(now);
        endDate.setDate(endDate.getDate() - 1);
    

        const formatDate = date => {
            const year = date.getFullYear();
            const month = String(date.getMonth() + 1).padStart(2, '0');
            const day = String(date.getDate()).padStart(2, '0');
            return `${year}${month}${day}`;
        };

        const startFormDate = formatDate(startDate);
        const formattedEndDate = formatDate(endDate);

        currentDateElement.textContent = `조회 가능 기간: ${startFormDate} ~ ${formattedEndDate}`;
    }
});

$(document).ready(function() {
    $('#dataForm').on('submit', function(event) {
        event.preventDefault();

        const date = $('#date').val();
        const time = $('#time').val();

        const requestData = {
            date: date,
            time: time
        };

        $.ajax({
            url: '/show_SK-data',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(requestData),
            success: function(response) {
                console.log('Success:', response);
                renderTable(response.final_exitData, '#tableContainer1', 'heading1');
                renderTable(response.final_carHeadCount_1, '#tableContainer2', 'heading2');
                renderTable(response.final_carHeadCount_4, '#tableContainer3', 'heading3');
                renderTable(response.final_congestionRatio_1, '#tableContainer4', 'heading4');
                renderTable(response.final_congestionRatio_4, '#tableContainer5', 'heading5');
                addDownloadButtons(requestData); // 버튼 추가
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

    function addDownloadButtons(requestData) {
        const buttonContainer = document.getElementById('buttonContainer');
        if (buttonContainer) {
            buttonContainer.innerHTML = '';

            const containers = ['#tableContainer1', '#tableContainer2', '#tableContainer3', '#tableContainer4', '#tableContainer5'];
            const buttonLabels = [
                'Exit Data <br>CSV 다운로드',
                '1호선 객차별 하차 비율 <br>CSV 다운로드',
                '4호선 객차별 하차 비율 <br> CSV 다운로드',
                '1호선 열차 혼잡도 <br> CSV 다운로드',
                '4호선 열차 혼잡도 <br> CSV 다운로드'
            ];
            const baseFileNames = [
                `ExitData`,
                `Line1_PassengerCount`,
                `Line4_PassengerCount`,
                `Line1_CongestionRatio`,
                `Line4_CongestionRatio`
            ];

            const dateTimeSuffix = `${requestData.date.replace(/-/g, '')}${requestData.time.replace(/:/g, '')}`;

            containers.forEach((selector, index) => {
                const button = document.createElement('button');
                const downloadCSVFileName = `${baseFileNames[index]}_${dateTimeSuffix}.csv`;

                button.innerHTML = buttonLabels[index] || `Download CSV ${index + 1}`;
                button.addEventListener('click', () => {
                    const table = document.querySelector(selector + ' table');
                    if (table) {
                        const csvContent = generateCSVFromTable(table);
                        downloadCSV(csvContent, downloadCSVFileName || `table_${index + 1}.csv`);
                    }
                });
                buttonContainer.appendChild(button);
            });
        }
    }

    function generateCSVFromTable(table) {
        let csv = [];
        const rows = table.querySelectorAll('tr');

        rows.forEach(row => {
            const cells = row.querySelectorAll('th, td');
            const rowContent = [];
            cells.forEach(cell => {
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
