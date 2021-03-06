import React, {useContext} from "react";
import { Link } from 'react-router-dom';
import AuthContext from "../context/auth-context";
import {ButtonSecondary} from "../components/Buttons";
import {useHistory} from "react-router-dom";

/**
 * A black link for the navbar (simply black text)
 * @param {string} to - The path to link to
 * @param {function} children - The text to display
 */
function NavbarLink(props){
    return (
        <Link to={props.to}>
            <div className="text-white text-xl font-semibold hover:underline transform translate-y-0 relative transition-all duration-200 ease-in-out hover:cursor-pointer hover:-translate-y-1">{props.children}</div>
        </Link>
    );
}

function Navbar(){
    const authContext = useContext(AuthContext);
    const history = useHistory();
    return (
        <div className="flex w-screen py-4 px-2 bg-primary items-center justify-center">
            <div className="flex flex-row items-center justify-between w-full max-w-1200">

                <div className="flex flex-row space-x-6 items-center">
                    <NavbarLink to="/"><h1 className="text-2xl font-bold">WordPath</h1></NavbarLink>
                    <NavbarLink to="/gamemodes">Gamemodes</NavbarLink>
                    <NavbarLink to="/register">Register</NavbarLink>
                </div>
                {authContext.loggedIn && 
                    <div className="flex flex-row space-x-4 items-center">
                        <span className="text-md text-white font-semibold">{`${authContext.userData?.exp.toFixed(0) || 0} EXP`}</span>
                    </div>
                }
                {!authContext.loggedIn && <ButtonSecondary onClick={() => history.push("/login")}>Login</ButtonSecondary>}
            </div>
        </div>
    );
}

export default Navbar;