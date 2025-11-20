import { motion } from "framer-motion";
import { Link } from "@tanstack/react-router";
import "../style.css";

export function SignUp() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.25, ease: "easeOut" }}
      className="min-h-screen flex flex-col items-center justify-center bg-gray-50 px-6"
    >
      {/* Title */}
      <motion.h1
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.05, duration: 0.25 }}
        className="
          text-4xl md:text-5xl
          font-semibold tracking-tight 
          text-center text-gray-900
          mb-14
        "
      >
        Continue as
      </motion.h1>

      {/* Card Background for Depth */}
      <div className="
        w-full max-w-md p-6
        bg-white rounded-2xl
        border border-gray-200
        shadow-sm
        flex flex-col gap-6
      ">
        {/* University Button */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.1, duration: 0.25 }}
        >
          <Link
            to="/signup/university"
            className="
              flex items-center justify-center
              w-full
              py-4 
              rounded-xl 
              text-lg font-medium
              bg-blue-500 text-white
              hover:bg-blue-600
              shadow-md hover:shadow-lg
              transition-all
              hover:-translate-y-0.5 active:translate-y-0
            "
          >
            University
          </Link>
        </motion.div>

        {/* Instructor Button */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.18, duration: 0.25 }}
        >
          <Link
            to="/signup/instructor"
            className="
              flex items-center justify-center
              w-full
              py-4
              rounded-xl 
              text-lg font-medium
              bg-indigo-500 text-white
              hover:bg-indigo-600
              shadow-md hover:shadow-lg
              transition-all
              hover:-translate-y-0.5 active:translate-y-0
            "
          >
            Instructor
          </Link>
        </motion.div>
      </div>

      {/* Footer */}
      <motion.p
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3, duration: 0.25 }}
        className="text-gray-600 mt-20 text-lg"
      >
        Already have an account?{" "}
        <Link
          to="/login"
          className="text-blue-600 hover:underline font-medium"
        >
          Login!
        </Link>
      </motion.p>
    </motion.div>
  );
}
