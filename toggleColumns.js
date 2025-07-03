function toggleCol(colIdx) {
    var table = document.getElementById('groups-table');
    for (var i = 0; i < table.rows.length; i++) {
        var cell = table.rows[i].cells[colIdx];
        if (cell) {
            cell.classList.toggle('hide-col');
        }
    }
}
