"use strict";



// const formData = {
//    read: $('#read').val(),
//    unread: $('#unread').val()
// }

$('.read').on('click', (evt) =>{
    // console.log(evt);
    // console.log(evt.currentTarget);
    
    // const formData = {
    //     read: $('#read').val(),
    //     unread: $('#unread').val()
    // }
    const bookId = $(evt.target).data('bookId');

    console.log(`Making request for book ID: ${bookId}`);

    $.post(`/set-read-status/${bookId}`, (res) => {
      console.log(`The book's status is now ${res.have_read}`);
      
    });
});