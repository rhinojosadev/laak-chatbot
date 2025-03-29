import { create  } from 'zustand';
import { devtools } from 'zustand/middleware'


export interface FormUser {
    name: string;
    position: string;
    company: string;
    closeModal: boolean;
}

interface Store {
    formUser: FormUser;
    setFormUser: (form: FormUser) => void;
    setField: (field:any, value: any) => void;
}

export const useLaakStore = create<Store>()(devtools((set: any) => ({
  formUser: {
    name: '',
    position: '',
    company: '',
    closeModal: false
  },
  setField: (field:any, value: any) => set((state: any) => ({
    formUser: { ...state.formUser, [field]: value } }
  )),
  resetForm: () =>
    set(() => ({
      formData: { name: '', email: '', message: '' }
    }))
})))