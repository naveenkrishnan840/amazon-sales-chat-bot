import React, { useState, useEffect, useRef } from "react";
import {TextareaAutosize} from "@mui/material";
import "react-chat-elements/dist/main.css"
import {MessageList } from "react-chat-elements";
import {Formik, Form, Field} from "formik";
import {RequestService} from "./request";
import parse from 'html-react-parser';

export default function ChatBotBody () {
    const [messages, setMessages] = useState([{
        position: "left",
        type: "text",
        title: "Bot",
        text: "Hi, How can i help you! I can assist you!",
        focus: true,
        className: "text-black max-h-screen font-semibold font-mono",
        date: new Date(),
        status: "received",
        avatar: "https://t4.ftcdn.net/jpg/02/11/61/95/360_F_211619589_fnRk5LeZohVD1hWInMAQkWzAdyVlS5ox.jpg",
        statusTitle: "Received"
        }]);
    const heightRef = useRef(null);
    const [isLoading, setIsLoading] = useState(false);
    const updateHeight = () => {
        if (heightRef.current) {
          heightRef.current.scrollTop = heightRef.current.scrollHeight;
        }
    };
    useEffect(() => {
        updateHeight();
    }, [messages]);
    const onSubmitForm = async (inputMessage) => {
        setIsLoading(true)
        const data = {"query": inputMessage["inputmessage"]};
        try {
            setIsLoading(true)
            const response = await fetch('http://127.0.0.1:8004/bot-message-request', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify(data) ,
            });
      
            const reader = response.body?.getReader();
            if (!reader) return;
      
            const decoder = new TextDecoder();
            while (true) {
                const { done, value } = await reader.read();
                if (done) break;
                let streamingMessage = decoder.decode(value, { stream: true });
                setIsLoading(false)
                setMessages((prevMsg)=>
                    [...prevMsg, {
                        position: "left",
                        type: "text",
                        title: "Bot",
                        text: parse(streamingMessage),
                        avatar: "https://t4.ftcdn.net/jpg/02/11/61/95/360_F_211619589_fnRk5LeZohVD1hWInMAQkWzAdyVlS5ox.jpg",
                        className: "text-black max-h-screen font-semibold font-mono",
                        date: new Date(),
                        statusTitle: "Received",
                        status: "received"
                    }]
                )
            }
        } catch (error) {
            console.error('Failed to send query:', error);
            setMessages(prev => [...prev, {
                type: 'error',
                content: 'Failed to connect to the server'
            }]);
        }
    }
    useEffect(() => {
        RequestService("/chatBotInitialize", [])
      }, []);
    return (
        <>
            <div className="relative ">
                <div className="w-auto h-14 my-1 shadow-md rounded-md p-2 text-wrap text-center font-mono font-extrabold size-4 text-lg text-white">
                    Amazon Sales Report Chat Bot
                </div>
                <div className="flex flex-col mx-40 rounded-md overflow-y-auto text-white shadow-lg" style={{height: "420px"}}>
                    <MessageList reference={heightRef} className="h-80 overflow-y-auto overflow-hidden " dataSource={messages} />
                </div>
                <Formik
                    validateOnBlur={false}
                    validateOnChange={false}
                        initialValues={{ inputmessage: ""}}
                        onSubmit={async (values, { resetForm }) => {
                            setMessages((prevMsg)=>
                                [...prevMsg, {
                                    position: "right",
                                    type: "text",
                                    title: "User",
                                    text: values.inputmessage,
                                    className: "text-black max-h-screen font-semibold font-mono",
                                    date: new Date(),
                                    status: "received",
                                    statusTitle: "Received",
                                    avatar: "https://t4.ftcdn.net/jpg/09/84/41/77/360_F_984417740_gYxjkB4WOCqAnZVvxLwVUPm7sEQK7hBQ.jpg"
                                }]
                            )
                            onSubmitForm(values)
                            resetForm({
                                values: { inputmessage: "",  passengerId: null}
                            })
                        }}
                        // validationSchema={}
                    >
                        {({ values, submitForm, errors }) => (
                            <Form>
                                <Field name="inputmessage" >
                                    {({ field }) => (
                                        <>
                                            <div className="group flex mx-40">
                                                <div style={{background: "#2f2f2f", border: "2px dashed white"}} className="flex w-full cursor-text flex-col rounded-xl px-2.5 py-1 contain-inline-size bg-[#f4f4f4] dark:bg-token-main-surface-secondary">
                                                    <div className="flex min-h-[44px] items-center px-2" style={{color: "white"}}>
                                                        <div className="max-w-full flex-1">
                                                            <div className="text-token-text-primary overflow-auto default-browser">
                                                                <TextareaAutosize disabled={isLoading} onChange={submitForm} {...field} style={{color: "white", maxHeight: "70px"}} className="chat-bot focus:outline-none block h-10 w-full resize-none border-0 bg-transparent px-0 py-2 text-token-text-primary placeholder:text-token-text-secondary" autoFocus="" placeholder="Message ChatGPT">
                                                                </TextareaAutosize>
                                                        </div>
                                                    </div>
                                                </div>
                                                <div className="flex h-[44px] items-center justify-between">
                                                    <div className="flex gap-x-1">
                                                        <div className="relative">
                                                            <div className="relative">
                                                                <div className="flex flex-col">
                                                                    <div type="button" aria-haspopup="dialog" aria-expanded="false" aria-controls="radix-:re:" data-state="closed"></div>
                                                                </div>
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <span data-state="closed">
                                                        <button disabled={isLoading} onSubmit={submitForm} aria-label="Send prompt" data-testid="send-button" className="flex h-8 w-8 items-center justify-center rounded-full transition-colors hover:opacity-70 focus-visible:outline-none focus-visible:outline-black disabled:text-[#f4f4f4] disabled:hover:opacity-100 dark:focus-visible:outline-white disabled:dark:bg-token-text-quaternary dark:disabled:text-token-main-surface-secondary bg-black text-white dark:bg-white dark:text-black disabled:bg-[#D7D7D7]">
                                                            <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg" className="icon-2xl"><path fillRule="evenodd" clipRule="evenodd" d="M15.1918 8.90615C15.6381 8.45983 16.3618 8.45983 16.8081 8.90615L21.9509 14.049C22.3972 14.4953 22.3972 15.2189 21.9509 15.6652C21.5046 16.1116 20.781 16.1116 20.3347 15.6652L17.1428 12.4734V22.2857C17.1428 22.9169 16.6311 23.4286 15.9999 23.4286C15.3688 23.4286 14.8571 22.9169 14.8571 22.2857V12.4734L11.6652 15.6652C11.2189 16.1116 10.4953 16.1116 10.049 15.6652C9.60265 15.2189 9.60265 14.4953 10.049 14.049L15.1918 8.90615Z" fill="currentColor"></path></svg>
                                                        </button>
                                                    </span>
                                                </div>
                                                </div>
                                            </div>
                                        </>
                                    )}
                                </Field>
                            </Form>)}
                </Formik>
            </div>
        </>
    )
}