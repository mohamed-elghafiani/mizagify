import Box from '@mui/material/Box';
import Modal from '@mui/material/Modal';
import { useContext, useEffect, useState } from 'react';
import AuthModalInputs from './AuthModalInputs';
import useAuth from '../hooks/useAuth';
import { Alert, CircularProgress } from '@mui/material';
import { UserContext } from '../contexts/userContext';
import { AuthenticationContext } from '../contexts/authContext';


const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 400,
  bgcolor: 'background.paper',
  boxShadow: 24,
  p: 4,
};


export default function AuthModal({isSignIn}) {
  const [open, setOpen] = useState(false);
  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);
  const {signin, signup} = useAuth()
  const {data, error, loading, setAuthState} = useContext(AuthenticationContext)
  
  const renderContent = (signInContent, signUpContent) => {
    return isSignIn ? signInContent : signUpContent
  }

  const [inputs, setInputs] = useState({
    first_name: "",
    last_name: "",
    email: "",
    phone: "",
    city: "",
    password: ""
  })

  // Disable submit button if fields are empty
  const [disable, setDisable] = useState(true)
  useEffect(() => {
    if(isSignIn) {
      if(inputs.password && inputs.email) {
        return setDisable(false)
      }
    } else {
      if(inputs.first_name && inputs.last_name && inputs.password && inputs.email && inputs.phone && inputs.city) {
        return setDisable(false)
      }
    }
    setDisable(true)
  }, [inputs])

  const handleChangeInput = (e) => {
    setInputs({
      ...inputs,
      [e.target.name]: e.target.value
    })
  }

  const handleClick = () => {
    if(isSignIn) {
      signin({email: inputs.email, password: inputs.password}, handleClose)
    } else {
      signup(inputs, handleClose)
    }
  }

  return (
    <div>
      <button className={`${renderContent("bg-primary text-white", "")} border border-primary p-1 px-4 rounded mr-3`} onClick={handleOpen}>
        {renderContent("Sign In", "Sign Up")}
      </button>
      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={style}>
          {loading ? (
            <div className="py-24 px-2 h-[500px] flex justify-center">
              <CircularProgress />
            </div>) : (<div className="p-2 h-[500px]">
            <div className="uppercase font-bold text-center pb-2 border-b mb-2">
              {error ? (
                <Alert severity="error" className="mb-4">{error}</Alert>) : null
              }
              <p className="text-sm">
                {renderContent("Sign In", "Create Account")}
                {data ? `City: ${data.city}` : null}
              </p>
            </div>
            <div className="m-auto">
              <h2 className="text-2xl font-light text-center">
                {renderContent("Log Into Your Account", "Create Your Account")}
              </h2>
              <AuthModalInputs inputs={inputs} handleChangeInput={handleChangeInput} isSignIn={isSignIn} />
              <button onClick={handleClick} className="uppercase bg-red-600 w-full text-white p-3 rounded text-sm mb-5 disabled:bg-gray-400" disabled={disable}>
                {renderContent("Sign In", "Create Account")}
              </button>
            </div>
          </div>)
          }
        </Box>
      </Modal>
    </div>
  );
}