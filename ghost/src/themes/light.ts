import { Theme, createTheme } from "@mui/material/styles";

export const themeLight: Theme = createTheme({
    palette: {
        mode: "light",
        primary: {
            main: "#ab47bc",
        },
        secondary: {
            main: "#263238",
        },
    },
});
