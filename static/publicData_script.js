

$(document).ready(function() {
    $('#dataForm').on('submit', function(event) {
        event.preventDefault(); // 기본 폼 제출을 방지

        const month = $('#month').val();
        const dow = $('#dow').val();
        const time = $('#time').val();

        const requestData = {
            month: month,
            dow: dow,
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
                addDownloadButtons(month, dow, time); // 버튼 추가
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

        data.sort((a, b) => {
            return exitSort(a.exit, b.exit);
        });

        const passengerKeys = ["승차인원", "하차인원"];

        data.forEach(item => {
            const row = $('<tr></tr>');
            for (const key in item) {
                const value = item[key];
                
                // 값 처리
                const displayValue = (passengerKeys.includes(key)) // 승차인원 또는 하차인원 열인 경우
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

    function exitSort(a, b) {
        const numA = parseInt(a.split('-')[0]); // "9-1" -> 9
        const numB = parseInt(b.split('-')[0]); // "10" -> 10
    
        if (numA === numB) {
            // 두 값이 동일한 경우 "9"와 "9-1"을 비교하여 "9"가 먼저 오도록 처리
            return a.includes('-') ? 1 : -1;
        }
        return numA - numB;
    }

    function addDownloadButtons(month, dow, time) {
        console.log('addDownloadButtons 호출됨');

        const buttonContainer = document.getElementById('buttonContainer');
        buttonContainer.innerHTML = '';
        const containers = ['#tableContainer1', '#tableContainer2'];
        const buttonLabels = [
            '1호선 승하차 인원 \nCSV 다운로드',
            '4호선 승하차 인원 \nCSV 다운로드'
        ];
        const fileNames = [
            `Line1_PassengerCount_${month}_${dow}_${time}.csv`,
            `Line4_PassengerCount_${month}_${dow}_${time}.csv`
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
