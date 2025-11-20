// src/pages/Home.tsx
import { motion, useAnimation } from "framer-motion";
import { Link } from "@tanstack/react-router";
import { PageTransition } from "../components/PageTransition";
import SplitText from "./SplitText";

export function Home() {
  const controls = useAnimation();

  const colors = [
    "#1677ff", 
    "#FACC15", 
    "#EF4444", 
    "#22C55E", 
    "#A855F7",
  ];

  let interval: any = null;

  function startInstantCycle() {
    let index = 0;
    interval = setInterval(() => {
      controls.start({
        backgroundColor: colors[index],
        transition: { duration: 0 },
      });
      index = (index + 1) % colors.length;
    }, 1500);
  }

  function stopCycle() {
    clearInterval(interval);
    controls.start({
      backgroundColor: "#1677ff",
      transition: { duration: 0.25 },
    });
  }

  return (
    <PageTransition>
      <div className="min-h-screen flex flex-col items-center justify-center px-6 bg-white">

        <SplitText
          text="Plagiarism Detection"
          className="text-8xl font-semibold text-center p-5"
          delay={40}
          duration={1}
          ease="power3.out"
          splitType="chars"
          from={{ opacity: 0, y: 40 }}
          to={{ opacity: 1, y: 0 }}
          threshold={0.1}
          rootMargin="-100px"
          textAlign="center"
        />

        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.15, duration: 0.25 }}
          className="text-gray-500 text-lg mt-4"
        >
          Academic plagiarism detection for universities & instructors
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 4 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.25, duration: 0.22 }}
          className="w-full max-w-xs mt-10"
        >
          <Link to="/login" className="block w-full">
            <motion.button
              animate={controls}
              onHoverStart={startInstantCycle}
              onHoverEnd={stopCycle}
              
              /* ⭐ iOS Hover Pop Effect */
              whileHover={{
                scale: 1.05,
                transition: { duration: 0.15, ease: "easeOut" }
              }}
              whileTap={{
                scale: 0.97
              }}

              className="
                w-full block
                h-14 rounded-xl
                text-lg font-medium text-white
                shadow-md hover:shadow-xl
                flex items-center justify-center
                select-none
                leading-none px-0
              "
              style={{
                backgroundColor: "#1677ff",
                color: "#ffffff",
              }}
            >
              Continue
            </motion.button>
          </Link>
        </motion.div>

      </div>
    </PageTransition>
  );
}
