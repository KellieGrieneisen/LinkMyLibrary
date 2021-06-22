"use strict";




$('.read').on('click', (evt) =>{
  
    const bookId = $(evt.target).data('bookId');

    console.log(`Making request for book ID: ${bookId}`);

    $.post(`/set-read-status/${bookId}`, (res) => {
      console.log(`The book's status is now ${res.have_read}`);
      
    });
});

let popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
  let popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
  return new bootstrap.Popover(popoverTriggerEl)
})