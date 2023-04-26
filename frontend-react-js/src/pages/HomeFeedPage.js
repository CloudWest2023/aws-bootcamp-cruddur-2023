import './HomeFeedPage.css';
import React from "react";

import DesktopNavigation  from '../components/DesktopNavigation';
import DesktopSidebar     from '../components/DesktopSidebar';
import ActivityFeed from '../components/ActivityFeed';
import ActivityForm from '../components/ActivityForm';
import ReplyForm from '../components/ReplyForm';

// Amplify
import { Auth } from 'aws-amplify';

// [TODO] Authenication
// import Cookies from 'js-cookie'

export default function HomeFeedPage() {
  const [activities, setActivities] = React.useState([]);
  const [popped, setPopped] = React.useState(false);
  const [poppedReply, setPoppedReply] = React.useState(false);
  const [replyActivity, setReplyActivity] = React.useState({});
  const [user, setUser] = React.useState(null);
  const dataFetchedRef = React.useRef(false);

  const loadData = async () => {
    try {
      console.log("HomeFeedPage - function 'loadData' started")
      console.log("React App Backend url: " + `${process.env.REACT_APP_BACKEND_URL}`)

      const backend_url = `${process.env.REACT_APP_BACKEND_URL}/api/activities/home`
      const res = await fetch(backend_url, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("access_token")}`
        },
        method: "GET"
      });
      let resJson = await res.json();
      if (res.status === 200) {
        setActivities(resJson)
      } else {
        console.log("Response: ", res)
      }
    } catch (err) {
      console.log(err);
    }
  };


  // check if we are authenicated
  const checkAuth = async () => {
    Auth.currentAuthenticatedUser({ // Checking to see if the user is authenticated
      // Optional, By default is false. 
      // If set to true, this call will send a 
      // request to Cognito to get the latest user data
      bypassCache: false 
    })
    .then((user) => {           // these bits are changed together. 
      console.log('user',user);
      return Auth.currentAuthenticatedUser() // return authenticated user
    }).then((cognito_user) => {   // if user is authenticated,  
        setUser({                 // set the user with the following authentication.
          display_name: cognito_user.attributes.name,
          handle: cognito_user.attributes.preferred_username
        })
    })
    .catch((err) => console.log(err));
  };

  // const checkAuth = async () => {
  //   console.log('checkAuth')
  //   // [TODO] Authenication
  //   if (Cookies.get('user.logged_in')) {
  //     setUser({
  //       display_name: Cookies.get('user.name'),
  //       handle: Cookies.get('user.username')
  //     })
  //   }
  // };


  React.useEffect(()=>{
    //prevents double call
    if (dataFetchedRef.current) return;
    dataFetchedRef.current = true;

    loadData();
    checkAuth();
  }, [])

  return (
    <article>
      <DesktopNavigation user={user} active={'home'} setPopped={setPopped} />
      <div className='content'>
        <ActivityForm  
          popped={popped}
          setPopped={setPopped} 
          setActivities={setActivities} 
        />
        <ReplyForm 
          activity={replyActivity} 
          popped={poppedReply} 
          setPopped={setPoppedReply} 
          setActivities={setActivities} 
          activities={activities} 
        />
        <ActivityFeed 
          title="Home" 
          setReplyActivity={setReplyActivity} 
          setPopped={setPoppedReply} 
          activities={activities} 
        />
      </div>
      <DesktopSidebar user={user} />
    </article>
  );
}