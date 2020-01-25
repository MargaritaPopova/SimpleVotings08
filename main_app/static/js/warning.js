function delete_warning() {
    let w = confirm('Вы действительно хотите удалить голосование? Это действие нельзя отменить!')
    if(w) {
        f = document.getElementById('voting_form');
        f.submit()
        }
}