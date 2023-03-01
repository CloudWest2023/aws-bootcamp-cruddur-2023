import './JoinSection.css';
import { Link } from "react-router-dom";

export default function JoinSection(props) {
  return (
    <div className="join">
      <div className='join-title'>
        <span>Join The Party! <img className='icon' src='/party-popper-svgrepo-com.svg' /></span>
      </div> 
      <div className='join-content'>
        <p className='passage' style={{'textAlign': 'left'}}>
          Have something you want to say? <br/>
          Don't think about it, just crud it! <br/>
          Regret it? No worries, We'll forget it...
        </p>
        <Link to="/signup" className="action">
          Join Now!
        </Link>
        <Link to="/signin" className="subaction">
          Sign In
        </Link>
      </div>
    </div>
  );
}