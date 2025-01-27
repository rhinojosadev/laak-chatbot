import { useState } from "react";
import {
  BotMessage,
  MyMessage,
  TextMessageBox,
  TypingLoader,
} from "./components";

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

  const handlePost = async (text: string) => {
    setIsLoading(true);
    setMessages((prev) => [...prev, { text, isBot: false }]);

    // TODO: Call API
    // const { ok, message } = await botService(text);
    // if (!ok) {
    //   setMessages((prev) => [
    //     ...prev,
    //     { text: "Hubo un error", isBot: true },
    //   ]);
    // } else {
    //   setMessages((prev) => [
    //     ...prev,
    //     {
    //       text: message,
    //       info: {
    //         message,
    //       },
    //       isBot: true,
    //     },
    //   ]);
    // }

    setIsLoading(false);
  };

  return (
    <main className="flex flex-row mt-7">
      <nav className="hidden sm:flex flex-col ml-5 w-[370px] min-h-[calc(100vh-3.0rem)] bg-white bg-opacity-10 p-5 rounded-3xl">
        <h1 className="font-bold text-lg lg:text-3xl bg-gradient-to-br from-white via-white/50 bg-clip-text text-transparent">
          Láak Chatbot
        </h1>

        <div className="border-gray-700 border" />
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
