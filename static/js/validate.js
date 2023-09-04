
function validator() {
    let st_dt = document.getElementById('dt_start').value;
    let en_dt = document.getElementById('dt_end').value;
    if ( st_dt == '' || en_dt == '') {
        alert('Date cannot be empty!')
        return;
    }
}

function fetch_img() {
    document.getElementById('img_playback').src = Flask.
}
document.addEventListener('DOMContentLoaded', function() {
    
    // date validator
    document.getElementById('btn_watch').addEventListener('click', () => {
        validator();
        fetch_img();
    });
});