import * as React from 'react';
import { Socket } from './Socket';



 


var login = false;
export class Content extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
        
        messageHolder : [],
        };
     
    }
    
    componentDidMount() {
           Socket.on('passedMessageList', (data) => {
        this.setState({
        messageHolder : data,
        });
        console.log(data);
    });
    }



handleSubmit(event) {
event.preventDefault();
var message = document.getElementById("sendMessageBox").value;
console.log(message);
Socket.emit('newMessage', message);
document.getElementById("sendMessageBox").value = " ";
}

   


    render() {
        let messageData = this.state.messageHolder.map(
            (n, index) => 
                <p key={index}><b>{n.message}</b>
                 <audio controls autoPlay>
                <source src={n.mediaLink} type="audio/mp3"></source></audio>
                </p>
            );

        return (
         
         
<div>
            <form onSubmit={this.handleSubmit}>
            <br />
           
             
                <h1>ChatBot Chat!</h1>
            <div>
            {messageData}
            </div>
                <input name="text" size="80" id="sendMessageBox" placeholder="enter message here"/>
                         <SubButton /> <br />
       
                </form>
              
           
     
         
                 </div>
        );
    }}
    
export class SubButton extends React.Component {
    render() {
        return (
            
                <button>Send it!</button>
           
        );
    }
}
export class ConnButton extends React.Component {
    render() {
        return (
            
                <button>Connect to chat!</button>
           
        );
    }
}
  export class DisConnButton extends React.Component {
    render() {
        return (
            
                <button>Disconnect from chat!</button>
           
        );
    }
}
  
  
    
