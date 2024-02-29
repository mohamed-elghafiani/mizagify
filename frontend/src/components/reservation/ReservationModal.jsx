import Box from '@mui/material/Box';
import Modal from '@mui/material/Modal';
import { useState } from 'react';
import ReservationCard from './ReservationCard';
import { BiTask } from 'react-icons/bi';


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


export default function ReservationModal({slug, open_time, close_time, imgs}) {
  const [open, setOpen] = useState(false);
  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  return (
    <div>
      <button className="mt-6 flex justify-between gap-2 items-center border border-sec text-2xl bg-primary px-4 py-2 rounded-xl text-white" onClick={handleOpen}>
        <BiTask />
        <span>Make a Reservation</span>
      </button>
      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={style}>
            <div className="m-auto">
              <ReservationCard slug={slug} open_time={open_time} close_time={close_time} imgs={imgs} />
            </div>
        </Box>
      </Modal>
    </div>
  );
}