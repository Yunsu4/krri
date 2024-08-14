document.addEventListener("DOMContentLoaded", function() {
    const currentDateElement = document.getElementById('currentDate');
    const now = new Date();
    
    // Add 1 day to today's date
    const nextDay = new Date(now);
    
    // Calculate the first day of the month for the next day
    const firstDayOfMonth  = new Date(nextDay.getFullYear(), nextDay.getMonth()-1, 1);

    const startDate = new Date(firstDayOfMonth);
    startDate.setDate(now.getDate() + 1);

    // Calculate the last day of the month for the next day
    const lastDayOfMonth = new Date(nextDay.getFullYear(), nextDay.getMonth() , 0);
    
    // Format dates as YYYYMMDD
    const formatDate = date => {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}${month}${day}`;
    };
    
    const startFormDate = formatDate(startDate);
    const endDate = formatDate(lastDayOfMonth);
    
    currentDateElement.textContent = `조회 가능 기간: ${startFormDate} ~ ${endDate}`;
});



document.getElementById('dataForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const date = document.getElementById('date').value;
    const time = document.getElementById('time').value;

    const requestData = {
        date: date,
        time: time
    }

    $.ajax({
        url: '/OD_Matrix',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(requestData),
        success: function(response) {
            const keysQuadrant1 = ["exit", "추정된 승차인원_1", "추정된 상행선 하차인원_1", "추정된 하행선 하차인원_1","추정된 승차인원_4", "추정된 상행선 하차인원_4",, "추정된 하행선 하차인원_4"]; // 원하는 키 목록
            const keysQuadrant2 = ['exit', '1-1','1-2','1-3','1-4','1-5','1-6','1-7','1-8','1-9','1-10',
                '2-1','2-2','2-3','2-4','2-5','2-6','2-7','2-8','2-9','2-10',
                '3-1','3-2','3-3','3-4','3-5','3-6','3-7','3-8','3-9','3-10',
                '4-1','4-2','4-3','4-4','4-5','4-6','4-7','4-8','4-9','4-10'];
                /*
            const keysQuadrant3 = ['exit', '1-1','1-2','1-3','1-4','1-5','1-6','1-8','1-9','1-10',
                '2-1','2-2','2-3','2-4','2-5','2-6','2-8','2-9','2-10',
                '3-1','3-2','3-3','3-4','3-5','3-6','3-8','3-9','3-10',
                '4-1','4-2','4-3','4-4','4-5','4-6','4-8','4-9','4-10'];
                */
            const keysQuadrant3 = ['platform', '1', '2', '3', ,'4', '5', '6', '7', '8', '9', '9-1', '10', 
                '11', '12', '13', '14', '15'];
                /*
            const keysQuadrant4 = ['1-1','1-2','1-3','1-4','1-5','1-6','1-7','1-8','1-9','1-10',
                '2-1','2-2','2-3','2-4','2-5','2-6','2-7','2-8','2-9','2-10',
                '3-1','3-2','3-3','3-4','3-5','3-6','3-7','3-8','3-9','3-10',
                '4-1','4-2','4-3','4-4','4-5','4-6','4-7','4-8','4-9','4-10'];
                */
            const keysQuadrant4 = [
                'platform','환승인원'
            ];
            const key1=["출구", "1호선 승차 인원", "1호선 상행선 하차 인원", "1호선 하행선 하차 인원", "4호선 승차 인원", "4호선 상행선 하차 인원", "4호선 하행선 하차 인원"
            ];
            const key2 = ["출구"];

            // 1호선 상행선 1번 객차부터 10번 객차까지 배열에 추가
            for (let i = 1; i <= 10; i++) {
                key2.push(`1호선 상행선 ${i}번 객차`);
            }
            for (let i = 1; i <= 10; i++) {
                key2.push(`1호선 하행선 ${i}번 객차`);
            }
            for (let i = 1; i <= 10; i++) {
                key2.push(`4호선 상행선 ${i}번 객차`);
            }
            for (let i = 1; i <= 10; i++) {
                key2.push(`4호선 하행선 ${i}번 객차`);
            }

            const key2_1 = key2.slice(1)

            const key3=["승강장", "1번 출구", "2번 출구", "3번 출구", "4번 출구", "5번 출구", "6번 출구", "7번 출구", "8번 출구", "9번 출구", "9-1번 출구",
                "10번 출구", "11번 출구", "12번 출구", "13번 출구", "14번 출구", "15번 출구"
            ];

            const key4=['승강장','환승인원'
            ];

            console.log('Response Data:', response); // Log the response to check its structure
            console.log('Key2 Length:', key2.length); // Log key2 length
            console.log('Data Length:', response.final_R4.length); // Log data length


            populateTable(response.final_R1, "#quadrant1", key1, keysQuadrant1, false);
            populateTable(response.final_R2, "#quadrant2", key2, keysQuadrant2, false);
            populateTable(response.final_R4, "#quadrant3", key3, keysQuadrant3, true, key2_1);
            populateTable(response.final_R5, "#quadrant4", key4, keysQuadrant4, true, key2_1);
        },
        error: function(error) {
            console.log('Error:', error);
        }
    });

function populateTable(data, selector, realkeys, keys, transepose, key2_1) {
    let table = '<table border="1">';

    if(transepose){
        // Create table headers
        table += '<thead><tr>';
        realkeys.forEach (key => {
            table += `<th>${key}</th>`;
        });
        table += '</tr></thead>';

        data.sort((a,b)=>{

            const aNum = extractExitNumber(a.platform);
            const bNum = extractExitNumber(b.platform);
            return aNum - bNum;
        })

        function extractExitNumber(exitValue) {
            // Assuming exitValue is in the format "4-1", "1-1", etc.
            const parts = exitValue.split('-');
            const firstPart = parseInt(parts[0]);
            const secondPart = parseInt(parts[1]);
            return firstPart * 100 + secondPart; // Multiply first part by 100 for proper sorting
        }

        // Create table rows
        table += '<tbody>';
        data.forEach((row, index) => {
            table += '<tr>';
            table += `<td>${key2_1[index]|| ''}</td>`; // Add value from key2 as the first column
                keys.slice(1).forEach(key => {
                    table += `<td>${row[key] === 0 ? 0 : 
                        (row[key] === null ? 0 : 
                        (typeof row[key] === 'number' ? (Math.ceil(row[key] * 100) / 100).toFixed(2) : row[key]))}</td>`;
                });
            
            table += '</tr>';
        });
        table += '</tbody>';


       

    }else{

        // Create table headers
        table += '<thead><tr>';
        realkeys.forEach (key => {
            table += `<th>${key}</th>`;
        });
        table += '</tr></thead>';

        // Create table rows
        table += '<tbody>';
        data.forEach(row => {
            table += '<tr>';
            keys.forEach (key => {
                table += `<td>${row[key] === 0 ? 0 : 
                    (row[key] === null ? 0 : 
                    (typeof row[key] === 'number' ? (Math.ceil(row[key] * 100) / 100).toFixed(2) : row[key]))}</td>`;
            });
            table += '</tr>';
        });
        table += '</tbody>';
    }
    table +='</table>';

    $(selector).html(table);
}

});
