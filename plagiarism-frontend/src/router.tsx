import { createRouter, createRootRoute, createRoute } from "@tanstack/react-router";
import { AppLayout } from "./layouts/AppLayout";
import { Home } from "./pages/Home";
import { Login } from "./pages/Login"
import { SignUp } from "./pages/SignUp"
import { UniversitySignUp } from "./pages/UniversitySignUp";
import { InstructorSignUp } from "./pages/InstructorSignUp";
import { AdminDashboard } from "./pages/AdminDashboard";

// General
const rootRoute = createRootRoute({
    component: AppLayout,
});

const indexRoute = createRoute({
    getParentRoute: () => rootRoute,
    path: "/",
    component: Home,
});

const loginRoute = createRoute({
    getParentRoute: () => rootRoute,
    path: "/login",
    component: Login,
})

const signupRoute = createRoute({
    getParentRoute: () => rootRoute,
    path: "/signup",
    component: SignUp,
})


// // Admin
const adminDashboard = createRoute({
    getParentRoute: () => rootRoute,
    path: "/admin",
    component: AdminDashboard,
});

// const adminLogin = createRoute({
//     getParentRoute: () => rootRoute,
//     path: "/admin/login",
//     component: AdminLogin,
// });

// const adminAccount = createRoute({
//     getParentRoute: () => rootRoute,
//     path: "/admin/account",
//     component: AdminAccount,
// });

// const adminUniversities = createRoute({
//     getParentRoute: () => rootRoute,
//     path: "/admin/universities",
//     component: AdminUniversities,
// });

// const adminPending = createRoute({
//     getParentRoute: () => rootRoute,
//     path: "/admin/pending",
//     component: AdminPending,
// });

// const adminReports = createRoute({
//     getParentRoute: () => rootRoute,
//     path: "/admin/reports",
//     component: AdminReports,
// });

// const adminActivities = createRoute({
//     getParentRoute: () => rootRoute,
//     path: "/admin/activities",
//     component: AdminActivities,
// });

// // University
// const universityDashboard = createRoute({
//     getParentRoute: () => rootRoute,
//     path: "/university",
//     component: UniversityDashboard,
// });

const universitySignUp = createRoute({
    getParentRoute: () => rootRoute,
    path: "/signup/university",
    component: UniversitySignUp,
});

// const universityLogin = createRoute({
//     getParentRoute: () => rootRoute,
//     path: "/university/login",
//     component: UniversityLogin,
// });

// const universityApproveInstructor = createRoute({
//     getParentRoute: () => rootRoute,
//     path: "/university/approve_instructor",
//     component: UniversityApproveInstructor,
// });

// const universityAccount = createRoute({
//     getParentRoute: () => rootRoute,
//     path: "/university/account",
//     component: UniversityAccount,
// });

// const universityUpload = createRoute({
//     getParentRoute: () => rootRoute,
//     path: "/university/upload",
//     component: UniversityUpload,
// });

// const universityInstructors = createRoute({
//     getParentRoute: () => rootRoute,
//     path: "/university/instructors",
//     component: UniversityInstructors,
// });

// const universityPending = createRoute({
//     getParentRoute: () => rootRoute,
//     path: "/university/pending",
//     component: UniversityPending,
// });

// const universityRepositories = createRoute({
//     getParentRoute: () => rootRoute,
//     path: "/university/repositories",
//     component: UniversityRepositories,
// });

// const universityRepository = createRoute({
//     getParentRoute: () => rootRoute,
//     path: "/university/repository/$id",
//     parseParams: (params) => ({
//         id: Number(params.id)
//     }),
//     component: UniversityRepository,
// });

// const universityRepositoryContent = createRoute({
//     getParentRoute: () => rootRoute,
//     path: "/university/repository/$id/content",
//     parseParams: (params) => ({
//         id: Number(params.id)
//     }),
//     component: UniversityErrors,
// });

// const universityRepositorySentence = createRoute({
//     getParentRoute: () => rootRoute,
//     path: "/university/repository/$id/$s_id",
//     parseParams: (params) => ({
//         id: Number(params.id),
//         s_id: Number(params.s_id),
//     }),
//     component: UniversityRepositorySentence,
// });

// const universityErrors = createRoute({
//     getParentRoute: () => rootRoute,
//     path: "/university/errors",
//     component: UniversityErrors,
// });

// // Instructor
// const instructorDashboard = createRoute({
//     getParentRoute: () => rootRoute,
//     path: "/instructor",
//     component: InstructorDashboard,
// });

const instructorSignUp = createRoute({
    getParentRoute: () => rootRoute,
    path: "/signup/instructor",
    component: InstructorSignUp,
});

// const instructorLogin = createRoute({
//     getParentRoute: () => rootRoute,
//     path: "/instructor/login",
//     component: InstructorLogin,
// });

// const instructorAccount = createRoute({
//     getParentRoute: () => rootRoute,
//     path: "/instructor/account",
//     component: InstructorAccount,
// });

// const instructorUpload = createRoute({
//     getParentRoute: () => rootRoute,
//     path: "/instructor/report/$id",
//     parseParams: (params) => ({
//         id: Number(params.id)
//     }),
//     component: InstructorUpload,
// });

// const instructorChecks = createRoute({
//     getParentRoute: () => rootRoute,
//     path: "/instructors/checks",
//     component: InstructorsChecks,
// });

// const instructorSubmissions = createRoute({
//     getParentRoute: () => rootRoute,
//     path: "/instructor/submissions",
//     component: InstructorSubmissions,
// });

// const instructorCheckReport = createRoute({
//     getParentRoute: () => rootRoute,
//     path: "/instructor/checks/$id",
//     parseParams: (params) => ({
//         id: Number(params.id)
//     }),
//     component: UniversityErrors,
// });

// const instructorCheckReferences = createRoute({
//     getParentRoute: () => rootRoute,
//     path: "/instructor/check/$id/references",
//     parseParams: (params) => ({
//         id: Number(params.id)
//     }),
//     component: InstructorCheckReferences,
// });

// const instructorCheckContent = createRoute({
//     getParentRoute: () => rootRoute,
//     path: "/instructor/check/$id/content",
//     parseParams: (params) => ({
//         id: Number(params.id)
//     }),
//     component: InstructorCheckContent,
// });

// const instructorCheckContentSentence = createRoute({
//     getParentRoute: () => rootRoute,
//     path: "/instructor/check/$id/sentence/$s_id",
//     parseParams: (params) => ({
//         id: Number(params.id),
//         s_id: Number(params.s_id),
//     }),
//     component: InstructorCheckContentSentence,
// });

// const instructorCheckDifference = createRoute({
//     getParentRoute: () => rootRoute,
//     path: "/instructor/checks/$id/difference",
//     parseParams: (params) => ({
//         id: Number(params.id)
//     }),
//     component: InstructorCheckDifference,
// });


const routeTree = rootRoute.addChildren([
    indexRoute,
    loginRoute,
    signupRoute,

    adminDashboard, // ← added ✔

    universitySignUp,
    instructorSignUp,
]);

export const router = createRouter({ routeTree });
declare module "@tanstack/react-router" {
    interface Register {
        router: typeof router;
    }
}
