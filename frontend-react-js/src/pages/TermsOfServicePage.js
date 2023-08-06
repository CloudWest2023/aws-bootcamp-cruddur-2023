import './TermsOfServicePage.css';
import React from "react";
import {ReactComponent as Logo} from 'components/svg/logo.svg';
import { Link } from "react-router-dom";

// // [TODO] Authenication
// import Cookies from 'js-cookie'

export default function TermsOfServicePage() {

  return (
    <article className="signin-article">
      <div className='signin-info'>
        <Logo className='logo' />
      </div>
      <div className='signin-wrapper'>
        <form 
          className='signin_form'
          onSubmit={onsubmit}
        >
          <h2 className='white-text'>Our Terms of Service</h2>
          <div className='white-text'>
            <div>
              <h3>Our Napkin of Service</h3>
                <img className='image-terms-of-service' src="/week00 logical diagram_white_gloria_gil.svg" alt="image" />  
                <br/>
                You can check it out <a className='link-text' href="https://lucid.app/lucidchart/invitations/accept/inv_38e40548-c558-46e2-aa36-f3e51ba96d6a" target={'_blank'} >here</a>
            </div>
            <div>
              <h3>Our Concept of Service</h3>
              <img className='image-terms-of-service' src="/week00 napkin diagram_white_gloria_gil.svg" alt="image" />  
                You can check it out <a href="https://lucid.app/lucidchart/invitations/accept/inv_f704a63f-078f-4728-8cc3-d1edebdf2910" target={'_blank'} rel="noreferrer">here</a>
            </div>
          </div>
        </form>
        <div className="dont-have-an-account">
          <span>
            Don't have an account?
          </span>
          <Link to="/signup">Sign up!</Link>
        </div>
      </div>

    </article>
  );
}