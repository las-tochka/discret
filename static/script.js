document.addEventListener('DOMContentLoaded', () => {
    const sizeInput = document.getElementById('size');
    const matrixContainer = document.getElementById('matrixContainer');
    const form = document.getElementById('graphForm');
    const matrixDataField = document.getElementById('matrixData');

function buildMatrix(size, prevData = '') {
    matrixContainer.innerHTML = '';
    const table = document.createElement('table');
    table.classList.add('no-borders');

    const dataRows = prevData.split('\n').map(row => row.trim().split(/\s+/));

    for (let i = 0; i < size; i++) {
        const tr = document.createElement('tr');
        for (let j = 0; j < size; j++) {
            const td = document.createElement('td');
            const input = document.createElement('input');
            input.type = 'number';
            input.min = '0';
            input.max = '1';
            input.className = 'form-control';
            input.name = `cell_${i}_${j}`;
            input.style.width = '50px';
            input.style.height = '50px';
            input.style.fontSize = '18px';
            input.style.textAlign = 'center';
            input.value = (dataRows[i] && dataRows[i][j]) ? dataRows[i][j] : '0';
            td.appendChild(input);
            tr.appendChild(td);
        }
        table.appendChild(tr);
    }

    matrixContainer.appendChild(table);
}


    if (sizeInput.value) {
        buildMatrix(parseInt(sizeInput.value), matrixDataField.value);
    }

    sizeInput.addEventListener('change', () => {
        const size = parseInt(sizeInput.value);
        if (size > 0) {
            buildMatrix(size);
        }
    });

    form.addEventListener('submit', (e) => {
        const size = parseInt(sizeInput.value);
        let matrix = [];

        for (let i = 0; i < size; i++) {
            let row = [];
            for (let j = 0; j < size; j++) {
                const input = document.querySelector(`input[name="cell_${i}_${j}"]`);
                row.push(input.value.trim() === '1' ? '1' : '0');
            }
            matrix.push(row.join(' '));
        }

        matrixDataField.value = matrix.join('\n');
    });
});
