export type Comparator =
    | "not_equals"
    | "equals"
    | "greater_than"
    | "less_than"
    | "greater_than_equal"
    | "less_than_equal";

type PluginFilter_Toggle = {
    type: "toggle";
    key: string;
    name: string;
    default: boolean;
};

type PluginFilter_Text = {
    type: "text";
    key: string;
    name: string;
    default: string;
};

type PluginFilter_Number = {
    type: "number";
    key: string;
    name: string;
    default: { comparator: Comparator; value: number };
};

type PluginFilter_Choice = {
    type: "choice";
    key: string;
    name: string;
    choices: { key: any; display: string }[];
    default: any | any[];
    multiple: boolean;
};

export type PluginFilter =
    | PluginFilter_Toggle
    | PluginFilter_Text
    | PluginFilter_Number
    | PluginFilter_Choice;

export type PluginManifest = {
    name: string;
    icon: {
        family: string;
        name: string;
    };
    version: string;
    author: string;
    source: string;
    filters: PluginFilter[];
    downloadOptions: PluginFilter[];
    entrypoint: {
        file: string;
        downloader: string;
    };
    requirements: string[];
    defaultConfig: any;
};
