import './PrivacyPolicyPage.css';
import React from "react";
import {ReactComponent as Logo} from 'components/svg/logo.svg';
import { Link } from "react-router-dom";

// [TODO] Authenication
import Cookies from 'js-cookie'

export default function PrivacyPolicyPage() {

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
          <h2>Our Privacy Policy</h2>
          <div className='fields'>
            <div className='field text_field username'>
              <h3 className='passage-title'>Privacy</h3>
              <p className='passage'>Shh... I can't tell you about our privacy policy, because you know, it's private!</p>
            </div>
          </div>
          <div className='submit'>
            <Link to="/forgot" className="forgot-link">Forgot Password?</Link>
            <button type='submit' title="This button does nothing. Just added for fun :D">Got it</button>
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