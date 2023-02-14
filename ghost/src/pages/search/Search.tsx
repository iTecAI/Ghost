import { useTheme } from "@mui/material";
import { Box } from "@mui/system";
import "./style.scss";

export function SearchPage() {
    const theme = useTheme();
    return (
        <Box
            className="search"
            sx={{ backgroundColor: theme.palette.background.default }}
        ></Box>
    );
}
