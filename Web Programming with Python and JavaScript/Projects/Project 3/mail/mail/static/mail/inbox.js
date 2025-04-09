document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  //submit handler
  document.querySelector('#compose-form').addEventListener('submit', send_email)

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-detail-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

}

function view_email(id){
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-detail-view').style.display = 'block';
    document.querySelector('#email-detail-view').innerHTML = `
      <ul class="list-group">
        <li class="list-group-item"><strong>From : </strong> ${email.sender}</li>
        <li class="list-group-item"><strong>To : </strong> ${email.recipients}</li>
        <li class="list-group-item"><strong>Subject : </strong> ${email.subject}</li>
        <li class="list-group-item"><strong>Timestamp : </strong> ${email.timestamp}</li>
        <li class="list-group-item">${email.body}</li>
      </ul>  
    `;
    if(!email.read){
      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
      })
    }
    
    //archive
    const element = document.createElement('button');
    element.innerHTML = email.archived ? "Unarchive" : "Archive"
    element.className = email.archived ? "btn btn-danger" : "btn btn-success"
    element.style.marginRight = "20px";
    element.addEventListener('click', function() {
      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: !email.archived
        })
      })
      .then(() =>{load_mailbox('archive')})
    });
    document.querySelector('#email-detail-view').append(element);

    //Reply
    const reply_btn  = document.createElement('button');
    reply_btn.innerHTML = "Reply"
    reply_btn.className = "btn btn-info"
    document.querySelector('#email-detail-view').append(reply_btn);
    
    reply_btn.addEventListener('click', function() {
      compose_email();
      document.querySelector('#compose-recipients').value = email.sender;
      let subject = email.subject;
      if (subject.split(' ', 1)[0] != "Re:"){
        subject = "Re: " + email.subject;
      }
      document.querySelector('#compose-subject').value = subject;
      document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote : ${email.body}`;
    })
});
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-detail-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  //Get the emails for the mailbox and user
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // Loop through emails and display
    emails.forEach(email => {
      const element = document.createElement('div');
      element.className = "list-group-item";
      element.innerHTML = `
        <h6>Sender : ${email.sender} </h6>
        <h5>Subject : ${email.subject} </h5>
        <p> ${email.timestamp}</p>
      `;
      //Change background color 
      element.className = email.read ? 'read' :"unread";
      element.addEventListener('click', function(){
        view_email(email.id)
      })
      document.querySelector('#emails-view').append(element);
    });
});
}
function send_email(event){
  event.preventDefault();
  // store fields
  const recipients = document.querySelector("#compose-recipients").value;
  const subject = document.querySelector("#compose-subject").value;
  const body = document.querySelector("#compose-body").value;
  
  //send data to backend

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
      load_mailbox('sent');
  });
}

