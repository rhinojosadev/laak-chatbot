import { useState } from "react";
import {
  BotMessage,
  MyMessage,
  TextMessageBox,
  TypingLoader,
} from "./components";
import { Modal } from "./components/modal/Modal";
import { useLaakStore } from "./components/store";

interface Message {
  text: string;
  isBot: boolean;
  info?: {
    message: string;
  };
}

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const { setField, formUser }  = useLaakStore();
  const API = "http://127.0.0.1:5000/api/v1/query";

  const handlePost = async (texto: string) => {
    setMessages((prev) => [
      ...prev,
       {
        text: texto,
        isBot: false
      }
    ])
    setIsLoading(true);
    try {
      const respuesta = await fetch(API, { 
        method: "POST",
        headers: {"Content-type": "application/json;charset=UTF-8"},
        body: JSON.stringify({
          pregunta: texto
        })
      });

      const data = await respuesta.json()

      setMessages((prev) => [
        ...prev,
         {
          text: texto,
          info: {
            message: data.response
          }, 
          isBot: true
        }
      ])
      setIsLoading(false);
    
    } catch (exception) {
      console.log(exception);
      setIsLoading(false);
    }

  };

  return (
    <main className="flex flex-row mt-7">
      <nav className="hidden sm:flex flex-col ml-5 w-[370px] min-h-[calc(100vh-3.0rem)] bg-white bg-opacity-10 p-5 rounded-3xl">
        <h1 className="font-bold text-lg lg:text-3xl bg-gradient-to-br from-white via-white/50 bg-clip-text text-transparent">
          Láak Chatbot
        </h1>

        <div className="border-gray-700 border" />
        { formUser.closeModal ? ( <>
         <p className="mt-8">Nombre: {formUser.name}</p>
         <p>Puesto: {formUser.position}</p>
         <p>Compañía: {formUser.company}</p> </>) : null }

      </nav>

      <section className="mx-3 sm:mx-20 flex flex-col w-full h-[calc(100vh-50px)]  bg-white bg-opacity-10 p-5 rounded-3xl">
        <div className="flex flex-row h-full">
          <div className="flex flex-col flex-auto h-full p-1">
            <div className="chat-container">
              <div className="chat-messages">
                <div className="grid grid-cols-12 gap-y-2">
                  <BotMessage text="Hola, ¿en qué puedo ayudarte?" />

                  {messages.map((message, index) =>
                    message.isBot ? (
                      <BotMessage key={index} text={message.info!.message} />
                    ) : (
                      <MyMessage key={index} text={message.text} />
                    )
                  )}

                  {isLoading && (
                    <div className="col-start-1 col-end-12 fade-in">
                      <TypingLoader />
                    </div>
                  )}
                </div>
              </div>
              {!formUser.closeModal ? (
                  <Modal 
                    header="Formulario Usuario"
                    description="Aqui va la descripcion y el texto"
                    onSubmit={() => {
                      setField("closeModal", true);
                    }}
                  >
                      <div className="mb-4">
                        <label className="text-sm text-gray-500">Nombre</label>
                        <input
                          value={formUser.name}
                          onChange={(e) =>{ 
                            e.preventDefault(); 
                            setField("name", e.target.value)
                          }}
                          type="text"
                          className="w-full px-4 py-2 mt-1 border rounded-lg focus:outline-none focus:ring-2 text-sm text-gray-500 focus:ring-blue-500"
                          placeholder="Ingrese su nombre"
                        />
                      </div>
                      <div className="mb-4">
                        <label className="text-sm text-gray-500">Puesto</label>
                        <input
                          type="text"
                          value={formUser.position}
                          onChange={(e) => { 
                            e.preventDefault(); 
                            setField("position", e.target.value); 
                          }}
                          className="w-full px-4 py-2 mt-1 border rounded-lg focus:outline-none focus:ring-2  text-sm  text-gray-500 focus:ring-blue-500"
                          placeholder="Ingrese su puesto"
                        />
                      </div>
                      <div className="mb-4">
                        <label className="text-sm text-gray-500">Empresa</label>
                        <input
                          type="text"
                          value={formUser.company}
                          onChange={(e) => setField("company", e.target.value)}
                          className="w-full px-4 py-2 mt-1 border rounded-lg focus:outline-none focus:ring-2  text-sm  text-gray-500 focus:ring-blue-500"
                          placeholder="Ingrese su empresa"
                        />
                      </div>
                  </Modal>
                    ): null}
              <TextMessageBox
                onSendMessage={handlePost}
                placeholder="Escribe aquí lo que deseas"
              />
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}

export default App;
