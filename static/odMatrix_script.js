
// 칸별 승차 인원까지만 구한 하나의 O-D Matrix를 위한 js



document.addEventListener("DOMContentLoaded", function() {
    
    document.getElementById('dataForm').addEventListener('submit', function(event) {

        $('.container').css('display', 'grid'); // container를 보이게 설정

    
        event.preventDefault();

        const month = document.getElementById('month').value;
        const dow = document.getElementById('dow').value;
        const time = document.getElementById('time').value;


        const requestData = {
            month: month,
            dow: dow,
            time: time
        }

        $.ajax({
            url: '/show_estimated-traffic',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(requestData),
            success: function(response) {
                const keysQuadrant1 = ["exit", "승차인원_1", "하차인원_1", "승차인원_4", "하차인원_4"];
                const keysQuadrant2 = ['exit', '1-1', '1-2', '1-3', '1-4', '1-5', '1-6', '1-7', '1-8', '1-9', '1-10',
                    '2-1', '2-2', '2-3', '2-4', '2-5', '2-6', '2-7', '2-8', '2-9', '2-10',
                    '3-1', '3-2', '3-3', '3-4', '3-5', '3-6', '3-7', '3-8', '3-9', '3-10',
                    '4-1', '4-2', '4-3', '4-4', '4-5', '4-6', '4-7', '4-8', '4-9', '4-10'];
                const keysQuadrant3 = ['platform', '1', '2', '3', '4', '5', '6', '7', '8', '9', '9-1', '10', 
                    '11', '12', '13', '14', '15'];
                const keysQuadrant4 = ['platform', '1-1', '1-2', '1-3', '1-4', '1-5', '1-6', '1-7', '1-8', '1-9', '1-10',
                    '2-1', '2-2', '2-3', '2-4', '2-5', '2-6', '2-7', '2-8', '2-9', '2-10',
                    '3-1', '3-2', '3-3', '3-4', '3-5', '3-6', '3-7', '3-8', '3-9', '3-10',
                    '4-1', '4-2', '4-3', '4-4', '4-5', '4-6', '4-7', '4-8', '4-9', '4-10'];
                const keysQuadrant5 = ['M00000', 'E00010', 'E00020', 'E00030', 'E00040', 'E00050', 'E00060', 'E00070', 
                    'E00080', 'E00090', 'E00091', 'E00100', 'E00110', 'E00120', 'E00130', 'E00140', 'E00150',
                    'T11001', 'T11002', 'T11003', 'T11004', 'T11005', 'T11006', 'T11007', 'T11008', 
                    'T11009', 'T11010', 'T12001', 'T12002', 'T12003', 'T12004', 'T12005', 'T12006', 
                    'T12007', 'T12008', 'T12009', 'T12010', 'T41001', 'T41002', 'T41003', 'T41004', 
                    'T41005', 'T41006', 'T41007', 'T41008', 'T41009', 'T41010', 'T42001', 'T42002', 
                    'T42003', 'T42004', 'T42005', 'T42006', 'T42007', 'T42008', 'T42009', 'T42010']
                   
                    
                const key1 = ["출구", "1호선 승차 인원", "1호선 하차 인원", "4호선 승차 인원", "4호선 하차 인원"];
                const key2 = ["출구"];
                const key4 = ["승강장"];
                const key5 = ['M00000', 'E00010', 'E00020', 'E00030', 'E00040', 'E00050', 'E00060', 'E00070', 
                    'E00080', 'E00090', 'E00091', 'E00100', 'E00110', 'E00120', 'E00130', 'E00140', 'E00150',
                    'T11001', 'T11002', 'T11003', 'T11004', 'T11005', 'T11006', 'T11007', 'T11008', 
                    'T11009', 'T11010', 'T12001', 'T12002', 'T12003', 'T12004', 'T12005', 'T12006', 
                    'T12007', 'T12008', 'T12009', 'T12010', 'T41001', 'T41002', 'T41003', 'T41004', 
                    'T41005', 'T41006', 'T41007', 'T41008', 'T41009', 'T41010', 'T42001', 'T42002', 
                    'T42003', 'T42004', 'T42005', 'T42006', 'T42007', 'T42008', 'T42009', 'T42010']
                   

                for (let i = 1; i <= 10; i++) {
                    key2.push(`1호선 상행선 ${i}번 객차`);
                    key4.push(`1호선 상행선 ${i}번 객차`);
                }
                for (let i = 1; i <= 10; i++) {
                    key2.push(`1호선 하행선 ${i}번 객차`);
                    key4.push(`1호선 하행선 ${i}번 객차`);
                }
                for (let i = 1; i <= 10; i++) {
                    key2.push(`4호선 상행선 ${i}번 객차`);
                    key4.push(`4호선 상행선 ${i}번 객차`);
                }
                for (let i = 1; i <= 10; i++) {
                    key2.push(`4호선 하행선 ${i}번 객차`);
                    key4.push(`4호선 하행선 ${i}번 객차`);
                }

                const key2_1 = key2.slice(1);


                const key3 = ["승강장", "1번 출구", "2번 출구", "3번 출구", "4번 출구", "5번 출구", "6번 출구", "7번 출구", "8번 출구", "9번 출구", "9-1번 출구",
                    "10번 출구", "11번 출구", "12번 출구", "13번 출구", "14번 출구", "15번 출구"];

                

                
                populateTable(response.final_R1, "#quadrant1", key1, keysQuadrant1, false);
                populateTable(response.final_R2, "#quadrant2", key2, keysQuadrant2, false);
                populateTable(response.final_R4, "#quadrant3", key3, keysQuadrant3, true, key2_1);
                populateTable(response.final_R5, "#quadrant4", key4, keysQuadrant4, true, key2_1);
                populateTable(response.final_oneMatrix, "#quadrant5", key5, keysQuadrant5, false);
                
                
                // Add CSV download buttons
                addDownloadButtons(requestData);
            },
            error: function(xhr, status, error) {
                console.log('AJAX Request Failed');
                console.log('Status:', status);
                console.log('Error Thrown:', error);
                console.log('Response Text:', xhr.responseText);
            }
        });

        function populateTable(data, selector, realkeys, keys, transpose, key2_1) {
            let table = '<table border="1">';


            if (transpose) {
                table += '<thead><tr>';
                realkeys.forEach(key => {
                    table += `<th>${key}</th>`;
                });
                table += '</tr></thead>';

                data.sort((a, b) => {
                    const aNum = extractExitNumber(a.platform);
                    const bNum = extractExitNumber(b.platform);
                    return aNum - bNum;
                });

                function extractExitNumber(exitValue) {
                    const parts = exitValue.split('-');
                    const firstPart = parseInt(parts[0]);
                    const secondPart = parseInt(parts[1]);
                    return firstPart * 100 + secondPart;
                }

                table += '<tbody>';
                data.forEach((row, index) => {
                    table += '<tr>';
                    table += `<td>${key2_1[index] || ''}</td>`;
                    keys.slice(1).forEach(key => {
                        if(row[key] !== 'number')
                            row[key]= parseFloat(row[key])
                        table += `<td>${row[key] === 0 ? 0 :
                            (row[key] === null ? 0 : (Math.round(row[key] * 1000) / 1000).toFixed(2))}</td>`;
                    });
                    table += '</tr>';
                });
                table += '</tbody>';

            } else {
                table += '<thead><tr>';
                realkeys.forEach(key => {
                    table += `<th>${key}</th>`;
                });
                table += '</tr></thead>';

                if (selector === "#quadrant5") {
                    const customOrder = ['E00010', 'E00020', 'E00030', 'E00040', 'E00050', 'E00060', 'E00070', 
                    'E00080', 'E00090', 'E00091', 'E00100', 'E00110', 'E00120', 'E00130', 'E00140', 'E00150',
                    'T11001', 'T11002', 'T11003', 'T11004', 'T11005', 'T11006', 'T11007', 'T11008', 
                    'T11009', 'T11010', 'T12001', 'T12002', 'T12003', 'T12004', 'T12005', 'T12006', 
                    'T12007', 'T12008', 'T12009', 'T12010', 'T41001', 'T41002', 'T41003', 'T41004', 
                    'T41005', 'T41006', 'T41007', 'T41008', 'T41009', 'T41010', 'T42001', 'T42002', 
                    'T42003', 'T42004', 'T42005', 'T42006', 'T42007', 'T42008', 'T42009', 'T42010'];

                    data.sort((a,b)=>{
                        const indexA = customOrder.indexOf(a['M00000']);
                        const indexB = customOrder.indexOf(b['M00000']);
                        return indexA - indexB;
                    })
                } else{
                    // 데이터 정렬 추가
                    data.sort((a, b) => {
                        return exitSort(a.exit, b.exit);
                    });
                }


                table += '<tbody>';
                data.forEach(row => {
                    table += '<tr>';
                    keys.forEach((key, index) => {
                        if(index === 0){
                            table += `<td>${row[key] || ''}</td>`;
                        }else{
                            if(row[key] !== 'number')
                                row[key]= parseFloat(row[key])
                                table += `<td>${row[key] === 0 ? 0 :
                                (row[key] === null ? 0 : (Math.round(row[key] * 1000) / 1000).toFixed(2))}</td>`;
                        }
                    });
                    table += '</tr>';
                });
                table += '</tbody>';
            }

            table += '</table>';

            document.querySelector(selector + ' .table-container').innerHTML = table;
            
        

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
        

        function addDownloadButtons(requestData) {
            const buttonContainer = document.getElementById('buttonContainer');
            buttonContainer.innerHTML = '';
            const quadrants = ['#quadrant1', '#quadrant2', '#quadrant3', '#quadrant4', '#quadrant5'];


            quadrants.forEach((selector, index) => {
                const button = document.createElement('button');
                const buttonLabels = [
                    '승하차 인원 \nCSV downlad',
                    '출발 통행 \nCSV downlad',
                    '도착 통행 \nCSV downlad',
                    '환승 통행 \nCSV downlad',
                    '전체 O-D Matrix \nCSV downlad'

                ];
                const baseFileNames = [
                    'PassengerCount',
                    'DepartureTraffic',
                    'ArrivalTraffic',
                    'TransferTraffic',
                    'O-D_Matrix'

                ];

                // 날짜와 시간으로 파일 이름을 구성
                const year = '2023'; // 고정된 연도
                const month = requestData.month || 'MM'; // 기본값 'MM'
                const dow = requestData.dow || 'DOW'; // 기본값 'DOW'
                const time = requestData.time || 'HH'; // 기본값 'HH'
                const dateTimeSuffix = `${year}_${month}_${dow}_${time}`;
                const downloadCSVFileName = `${baseFileNames[index]}_${dateTimeSuffix}.csv`;


                
                button.textContent = buttonLabels[index] || `Download CSV ${index + 1}`;
                button.addEventListener('click', () => {
                    const table = document.querySelector(selector + ' table');
                    const csvContent = generateCSVFromTable(table);
                    downloadCSV(csvContent, downloadCSVFileName || `quadrant_${index + 1}.csv`);
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
            csvContent = BOM+csvContent
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
});
