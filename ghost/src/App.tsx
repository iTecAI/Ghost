import { CssBaseline, ThemeProvider } from "@mui/material";
import React, { createContext, ReactNode, useState } from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import "./App.scss";
import { SearchPage } from "./pages/search/Search";
import { themeDark } from "./themes/dark";
import { themeLight } from "./themes/light";
import i18n from "i18next";
import { initReactI18next } from "react-i18next";

import * as locEn from "./localization/en.json";

const ThemeContext = createContext<
    ["dark" | "light", (theme: "dark" | "light") => void]
>(["dark", (theme) => {}]);
function Theming(props: { children: ReactNode }) {
    const [theme, setTheme] = useState<"dark" | "light">(
        (localStorage.getItem("theme") as "dark" | "light") ?? "dark"
    );
    return (
        <ThemeContext.Provider value={[theme, setTheme]}>
            <CssBaseline />
            <ThemeProvider theme={theme === "dark" ? themeDark : themeLight}>
                {props.children}
            </ThemeProvider>
        </ThemeContext.Provider>
    );
}

i18n.use(initReactI18next) // passes i18n down to react-i18next
    .init({
        // the translations
        // (tip move them in a JSON file and import them,
        // or even better, manage them via a UI: https://react.i18next.com/guides/multiple-translation-files#manage-your-translations-with-a-management-gui)
        resources: {
            en: {
                translation: locEn,
            },
        },
        lng: "en", // if you're using a language detector, do not define the lng option
        fallbackLng: "en",

        interpolation: {
            escapeValue: false, // react already safes from xss => https://www.i18next.com/translation-function/interpolation#unescape
        },
    });

function App() {
    return (
        <Theming>
            <BrowserRouter>
                <Routes>
                    <Route index element={<SearchPage />} />
                </Routes>
            </BrowserRouter>
        </Theming>
    );
}
export default App;
