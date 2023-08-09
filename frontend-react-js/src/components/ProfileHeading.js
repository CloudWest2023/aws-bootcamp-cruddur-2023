import './ProfileHeading.css';
import EditProfileButton from './EditProfileButton';

export default function ProfileHeading(props) {
    const backgroundImage = 'url("https://avatars.goodstuff.cloud/banners/background.png")'
    const styles = {
        backgroundImage: backgroundImage,
        backgroundSize: 'cover',
        backgroundPosition: 'center'
    }

    return (
        <div className='activity_feed_heading profile_heading'>
            <div className='banner' style={styles} />
            <div className='container-user-info'>
                <div className='container-avatar'>
                    <img className='avatar' src="https://avatars.goodstuff.cloud/avatars/mariachi-behind-the-helm.png" />
                    {/* <div className='container-avatar'>
                    </div> */}
                </div>
                <div className='container-info'>
                    <div className='id-info'>
                        <div>
                            <div className='title'>{props.profile.display_name}</div>
                            <div className='cruds_count'>{props.profile.cruds_count} stuffs</div>
                        </div>
                        <div>
                            <EditProfileButton setPopped={props.setPopped} />
                        </div>
                    </div>
                </div>
            </div>
            <div className='bio'>Bio: {props.profile.bio}</div>
        </div>
    );
}