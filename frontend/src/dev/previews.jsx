import {ComponentPreview, Previews} from '@react-buddy/ide-toolbox'
import {PaletteTree} from './palette'
import Login from "../pages/Login.jsx";

const ComponentPreviews = () => {
    return (
        <Previews palette={<PaletteTree/>}>
            <ComponentPreview path="/Login">
                <Login/>
            </ComponentPreview>
        </Previews>
    )
}

export default ComponentPreviews