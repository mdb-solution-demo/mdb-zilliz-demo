import React, { useState, useEffect, useContext, useRef } from "react";
import { queryContext } from "../contexts/QueryContext";
import { createStyles, Theme, makeStyles } from "@material-ui/core/styles";
import useMediaQuery from "@material-ui/core/useMediaQuery";
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";
import Fab from "@material-ui/core/Fab";
import AddIcon from "@material-ui/icons/Add";
import CloseIcon from "@material-ui/icons/Close";
import Slider from "@material-ui/core/Slider";
import { DropzoneArea } from "material-ui-dropzone";
import SeperatLine from "../components/SeperatLine";
import { baseColor } from "../utils/color";
import Logo from "./Logo.svg";
import { delayRunFunc } from "../utils/Helper";
import {UploadIcon} from '../components/Icons'

let timer:any = undefined;

const Setting = (props: any) => {
  const isMobile = !useMediaQuery("(min-width:1000px)");
  const useStyles = makeStyles((theme: Theme) => {
    return createStyles({
      setting: {
        display: "flex",
        flexDirection: "column",
        minWidth: isMobile ? "90%" : "300px",
        padding: "60px 20px",
        borderWidth: "1px",
        backgroundColor: "#1F2023",
        color: "#E4E4E6",
        overflowY: "auto",
      },
      header: {
        marginBottom: "30px",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
      },
      configHead: {
        marginBottom: "30px",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
      },
      config: {
        fontSize: "24px",
        color: "#FAFAFA",
      },
      clear: {
        color: baseColor,
        fontSize: "18px",
        cursor: "pointer",
      },
      imageSet: {},
      counts: {
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        marginBottom: "30px",
        color: "#FAFAFA",
      },
      currTotal: {
        fontSize: "12px",
      },
      setPath: {
        display: "flex",
        justifyContent: "start",
        alignItems: "center",
        marginBottom: "30px",
      },
      customInput: {
        margin: "0 20px 0 0 !important",
        color: "blue !important",
        width: isMobile ? "80%" : "auto",
      },
      customTextInput: {
        margin: "0 20px 20px 0 !important",
        color: "blue !important",
        width: isMobile ? "80%" : "auto",
      },
      customFab: {
        color: "#fff",
        backgroundColor: baseColor,
        width: "36px",
        height: "36px",
        "&:hover": {
          backgroundColor: baseColor,
        },
      },
      customDeleteFab: {
        position: "absolute",
        top: "5px",
        right: "5px",
        color: "#fff",
        backgroundColor: "#666769",
        width: "24px",
        height: "24px",
        minHeight: "0px",
        "&:hover": {
          backgroundColor: "#666769",
        },
      },
      customDelete: {
        color: "#A7A7AF",
        width: "18px",
        height: "18px",
      },
      customIcon: {
        color: "#fff",
        backgroundColor: baseColor,
        width: "20px",
        height: "20px",
      },
      customSlider: {
        color: baseColor,
        marginBottom: "10px",
      },
      thumb: {
        width: "16px",
        height: "16px",
      },
      track: {
        height: "4px",
        borderRadius: "10px",
      },
      upload: {
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      },
      benchImage: {
        width: "400px",
        height: "250px",
        position: "relative",
      },
      dropzoneContainer: {
        backgroundColor: "transparent",
        width: "250px",
        height: "250px",
        borderRadius: "10px",
        border: "solid .5px #C8C8C8",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      },
      dropzoneText: {
        fontSize: "14px",
        color: "#B3B4B5",
        marginBottom: "30px",
      },
      notchedOutline: {
        borderWidth: ".5px",
        borderColor: "#838385 !important",
      },
      formLabel: {
        color: "#fff",
      },
      controlLabel: {
        color: "#838385",
      },

      uploaderWrapper: {
        width: '250px',
        height: '250px',
        borderRadius: '10px',
        border: "1px solid #ccc",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        cursor: "pointer",

        '&:hover': {
          borderColor: "#fff"
        },

        '& >p': {
          fontSize: "14px",
          lineHeight: "20px",
          color: '#B3B4B5',
          marginBottom: '30px'
          },

        "& > svg": {
          width: "60px",
          hight: "60px"
        },
      },
      customerUploader: {
          position: "absolute",
          zIndex: -1000,
          visibility: "hidden",
          opacity: "0"
      }
    });
  });
  const {  search,searchText } = useContext(queryContext);
  const { setImages, loading, setLoading } = props;
  const classes = useStyles({});
  const [inputs, setInputs]: any = useState("");
  const [topK, setTopK]: any = useState(5);
  const [image, setImage]: any = useState();
  const [searchingText, setSearchingText] = useState('');
  const imgFileCache = useRef<any>(null);

  const fileUploader = useRef<HTMLInputElement | null>(null);

  const reader = new FileReader();
  reader.addEventListener(
    "load",
    function () {
      imgFileCache.current = reader.result;
    },
    false
  );

  const handleSearchImg = async(file:File) => {
    setLoading(true)
   
    const fd = new FormData();
    fd.set("topk", topK);
    fd.append("image", file);
    try {
      const res = await search(fd);
      const { status, data } = res || {};
      setImages(data);
    }finally {
      setLoading(false)
    }
  };

  const handleUploadImg = ()=>{
    if(!fileUploader.current){
      return
    }
    fileUploader.current.click();
  }
  const handleImgChange= async (e:React.ChangeEvent<HTMLInputElement>)=>{
    if(!e.target.files) {
      return
    }
    const file = e.target.files[0];
    const url = URL.createObjectURL(file)
    setImage(url);
    setSearchingText('');
    imgFileCache.current = file;
    handleSearchImg(file)
    
  }

  const onSearchTextChange = async(e:React.ChangeEvent<HTMLInputElement |HTMLTextAreaElement>)=>{
    const val = e.target.value;
    setSearchingText(val)    
    setImage(null)
    imgFileCache.current = null
    
  }

  const handleSearchText = async()=>{
    if(!searchingText.trim()) {
      return
    }
    setLoading(true)
    try {
      const res =  await searchText({text:searchingText, topK});
      const { status, data } = res || {};
      setImages(data);
      
    }finally {
      setLoading(false)
    }
    
  }

  const onTopKChange = (e: any, val: any) => {
    setTopK(val);
    if(searchingText) {
      delayRunFunc( handleSearchText, 300);
      return
    }
    if (image) {
      const file = imgFileCache.current;
      delayRunFunc( handleSearchImg, 300,file);
      return
    }

  };


  return (
    <div className={classes.setting}>
      <div className={classes.header}>
        <img src={Logo} width="150px" alt="logo" />
        <h3>
          MongoDB & Zilliz Integration Search Demo
        </h3>
      </div>
      <SeperatLine title={`Text To Search`} style={{ marginBottom: "20px" }} />
      <div>
        <TextField
          classes={{ root: classes.customTextInput }}
          label=""
          variant="outlined"
          onChange={onSearchTextChange}
          InputLabelProps={{
            shrink: true,
            classes: {
              root: classes.controlLabel,
              focused: classes.controlLabel,
            },
          }}
          margin="normal"
          InputProps={{
            style: {
              textAlign: "left",
              width: isMobile ? "100%" : "340px",
              height: "40px",
            },
            classes: {
              notchedOutline: classes.notchedOutline,
              root: classes.formLabel,
            },
            placeholder: "Search text",
          }}
        />
        <Button variant="contained" onClick={handleSearchText}>Search</Button>
      </div>

      <SeperatLine title={`IMAGE To Search`} style={{ marginBottom: "20px" }} />
      <div className={classes.upload}>
        {image ? (
          <div className={classes.benchImage}>
            <img

              className={classes.benchImage}
              src={image}
              alt="..."
            />
            <Fab
              color="primary"
              aria-label="add"
              size="small"
              classes={{ root: classes.customDeleteFab }}
            >
              <CloseIcon
                onClick={() => {
                  setImage();
                  setImages([]);
                }}
                classes={{ root: classes.customDelete }}
              />
            </Fab>
          </div>
        ) : (
          <div className="">
            <div className={classes.uploaderWrapper} onClick={handleUploadImg}>
              <p>Click to upload</p>
              <UploadIcon />
            </div>
            <input type="file" name="" id="" ref={fileUploader} onChange={handleImgChange} className={classes.customerUploader} />
          </div>
        )}
      </div>

      {/* <div className={classes.configHead}>
        <h4 className={classes.config}>Config</h4>
        <h4 className={classes.clear} onClick={clear}>
          CLEAR ALL
        </h4>
      </div> */}
      <SeperatLine title={`TOP K(1－100)`} style={{ marginTop: "20px" }} />
      <div className={classes.counts}>
        <p>{`show top ${topK} results`}</p>
      </div>
      <Slider
        min={1}
        max={100}
        value={topK}
        onChange={onTopKChange}
        classes={{
          root: classes.customSlider,
          track: classes.track,
          rail: classes.track,
          thumb: classes.thumb,
        }}
      />

     
    </div>
  );
};

export default Setting;
