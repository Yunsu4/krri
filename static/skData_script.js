 $(document).ready(function() {
    $('#dataForm').on('submit', function(event) {
        event.preventDefault();

        const dow = $('#dow').val();
        const time = $('#time').val();

        const requestData = {
            dow: dow,
            time: time
        };

        $.ajax({
            url: '/show_SK-data',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(requestData),
            success: function(response) {
                console.log('Success:', response);
                renderTable(response.final_carHeadCount_1, '#tableContainer1', 'heading1');
                renderTable(response.final_carHeadCount_4, '#tableContainer2', 'heading2');
                renderTable(response.final_congestionRatio_1, '#tableContainer3', 'heading3');
                renderTable(response.final_congestionRatio_4, '#tableContainer4', 'heading4');
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


        const particularKeys = ["ratio", "congestion"];

        data.forEach(item => {
            const row = $('<tr></tr>');
            for (const key in item) {
                const value = item[key];
                
                // 값 처리
                const displayValue = (particularKeys.includes(key)) // 특정한 열인 경우
                ? (value === null ? 0 : isNaN(parseFloat(value)) ? value : parseFloat(value).toFixed(2)) // 숫자인 경우 소수점 둘째 자리까지 포맷
                : (value === null ? 0 : value); // 기타 열은 그대로 표시
                
                // 행에 셀 추가
                row.append($('<td></td>').text(displayValue));
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

            const containers = ['#tableContainer1', '#tableContainer2', '#tableContainer3', '#tableContainer4'];
            const buttonLabels = [
                '1호선 객차별 하차 비율 <br>CSV 다운로드',
                '4호선 객차별 하차 비율 <br> CSV 다운로드',
                '1호선 열차 혼잡도 <br> CSV 다운로드',
                '4호선 열차 혼잡도 <br> CSV 다운로드'
            ];
            const baseFileNames = [
                `Line1_PassengerCount`,
                `Line4_PassengerCount`,
                `Line1_CongestionRatio`,
                `Line4_CongestionRatio`
            ];


            const dow = requestData.dow || 'DOW'; // 기본값 'DOW'
            const time = requestData.time || 'HH'; // 기본값 'HH'
            const dateTimeSuffix = `${dow}_${time}`;

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
/*
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
*/

function generateCSVFromTable(table) {
    let csv = [];
    const rows = table.querySelectorAll('tr');

    rows.forEach(row => {
        const cells = row.querySelectorAll('th, td');
        const rowContent = [];
        cells.forEach(cell => {
            let cellText = cell.textContent.trim();

            // 셀 내용이 쉼표를 포함하는 경우 따옴표로 감싸기
            if (cellText.includes(',')) {
                cellText = `"${cellText}"`;
            }

            rowContent.push(cellText);
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
