function delete_warning() {
    let w = confirm('Вы действительно хотите удалить голосование? Это действие нельзя отменить!')
    if(w) {
        b = document.getElementById('delete');
        console.log(b)
        b.submit()
        }
}